<?php
/**
 * lux-taxi.com — Traitement du formulaire de devis
 * 1. Enregistre chaque demande dans api/data/demandes.csv (rien ne se perd)
 * 2. Envoie la demande par e-mail à info@lux-taxi.com
 * 3. Ne répond "succès" au visiteur que si l'e-mail est vraiment parti
 */

header('Content-Type: application/json; charset=utf-8');

const DESTINATAIRE = 'info@lux-taxi.com';
const EXPEDITEUR   = 'info@lux-taxi.com';
const TELEPHONE    = '+41 76 620 78 50';
const DOSSIER_DATA = __DIR__ . '/data';

function repondre(int $code, array $data): void {
    http_response_code($code);
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    exit;
}

// Texte sur une ligne : sans balises, sans retours à la ligne (anti-injection d'en-têtes), longueur limitée
function ligne($v, int $max = 200): string {
    $v = is_string($v) ? $v : '';
    $v = strip_tags($v);
    $v = preg_replace('/[\x00-\x1F\x7F]+/u', ' ', $v);
    return mb_substr(trim($v), 0, $max);
}

// Texte multiligne : sans balises, longueur limitée
function bloc($v, int $max = 3000): string {
    $v = is_string($v) ? $v : '';
    $v = strip_tags($v);
    $v = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]+/u', '', $v);
    return mb_substr(trim($v), 0, $max);
}

function h(string $v): string {
    return htmlspecialchars($v, ENT_QUOTES, 'UTF-8');
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    repondre(405, ['success' => false, 'error' => 'Méthode non autorisée.']);
}

$input = json_decode(file_get_contents('php://input'), true);
if (!is_array($input)) { $input = $_POST; }

// Anti-spam : champ invisible rempli = robot (on fait semblant d'accepter)
if (!empty($input['website_check'])) {
    repondre(200, ['success' => true]);
}

if (!is_dir(DOSSIER_DATA)) { @mkdir(DOSSIER_DATA, 0750, true); }

$d = [
    'nom'          => ligne($input['name'] ?? '', 120),
    'societe'      => ligne($input['company'] ?? '', 120),
    'email'        => filter_var(ligne($input['email'] ?? '', 160), FILTER_VALIDATE_EMAIL) ?: '',
    'telephone'    => ligne($input['phone'] ?? '', 40),
    'prestation'   => ligne($input['service'] ?? '', 120),
    'vehicule'     => ligne($input['fleet'] ?? '', 120),
    'date'         => ligne($input['date'] ?? '', 20),
    'heure'        => ligne($input['time'] ?? '', 10),
    'depart'       => ligne($input['pickup'] ?? '', 200),
    'destination'  => ligne($input['dropoff'] ?? '', 200),
    'message'      => bloc($input['message'] ?? ''),
];

// Contrôles (nov. 2026) : nom, départ, arrivée, date future, téléphone valable ; e-mail facultatif mais valable s'il est donné
function telephoneValable(string $t): string {
    $c = preg_replace('/[\s.\-()\/]/', '', $t);
    if (strpos($c, '00') === 0) { $c = '+' . substr($c, 2); }
    if (preg_match('/^\+[1-9]\d{7,14}$/', $c) || preg_match('/^0[1-9]\d{8}$/', $c)) {
        $chiffres = preg_replace('/\D/', '', $c);
        if (count(array_unique(str_split($chiffres))) >= 3) { return $c; }
    }
    return '';
}
function emailValable(string $e): bool {
    if (!filter_var($e, FILTER_VALIDATE_EMAIL) || !preg_match('/@[^@\s]+\.[a-z]{2,}$/i', $e)) { return false; }
    $domaine = substr(strrchr($e, '@'), 1);
    // Le domaine doit exister (si le serveur arrive à vérifier : test sur gmail.com d'abord, pour ne jamais perdre un client)
    if (function_exists('checkdnsrr') && @checkdnsrr('gmail.com', 'MX')) {
        if (!@checkdnsrr($domaine, 'MX') && !@checkdnsrr($domaine, 'A')) { return false; }
    }
    return true;
}
$erreurs = [];
$emailBrut = ligne($input['email'] ?? '', 160);
$d['email'] = '';
if ($d['nom'] === '') { $erreurs['name'] = 'Please enter your name.'; }
if ($d['depart'] === '') { $erreurs['from'] = 'Please enter a pick-up place.'; }
if ($d['destination'] === '') { $erreurs['to'] = 'Please enter a drop-off place.'; }
$quand = (preg_match('/^\d{4}-\d{2}-\d{2}$/', $d['date']) && preg_match('/^\d{2}:\d{2}$/', $d['heure'])) ? strtotime($d['date'] . ' ' . $d['heure'] . ' Europe/Zurich') : false;
if (!$quand) { $erreurs['when'] = 'Please choose a date and time.'; }
elseif ($quand < time() - 3600) { $erreurs['when'] = 'Please choose a date and time in the future.'; }
$tel = telephoneValable($d['telephone']);
if ($tel === '') { $erreurs['phone'] = 'Please enter a valid phone number, e.g. +41 79 123 45 67.'; } else { $d['telephone'] = $tel; }
if ($emailBrut !== '') {
    if (emailValable($emailBrut)) { $d['email'] = $emailBrut; } else { $erreurs['email'] = 'This email address does not look valid.'; }
}
if ($erreurs) {
    repondre(422, ['success' => false, 'error' => 'Please check the highlighted fields.', 'fields' => $erreurs]);
}
// Anti-abus : 5 demandes max par adresse IP et par tranche de 10 minutes
$ip = $_SERVER['REMOTE_ADDR'] ?? 'inconnue';
$fichierLimite = DOSSIER_DATA . '/limite_' . hash('sha256', $ip) . '.txt';
$maintenant = time();
$historique = [];
if (is_file($fichierLimite)) {
    $historique = array_filter(
        array_map('intval', explode("\n", (string) @file_get_contents($fichierLimite))),
        fn($t) => $t > $maintenant - 600
    );
}
if (count($historique) >= 5) {
    repondre(429, ['success' => false, 'error' => 'Too many requests in a short time. Please message us on WhatsApp or call ' . TELEPHONE . '.']);
}
$historique[] = $maintenant;
@file_put_contents($fichierLimite, implode("\n", $historique), LOCK_EX);

// Position GPS envoyée par le bouton « Use my location » : lien carte ajouté au message
$lat = filter_var($input['lat'] ?? null, FILTER_VALIDATE_FLOAT);
$lng = filter_var($input['lng'] ?? null, FILTER_VALIDATE_FLOAT);
if ($lat !== false && $lng !== false && $lat !== null && $lng !== null && abs($lat) <= 90 && abs($lng) <= 180) {
    $lien = 'https://maps.google.com/?q=' . round($lat, 6) . ',' . round($lng, 6);
    $d['message'] = trim('Position GPS du client (départ) : ' . $lien . "\n" . $d['message']);
}

// 1. Enregistrement de la demande (avant l'envoi, pour ne jamais la perdre)
$csv = DOSSIER_DATA . '/demandes.csv';
$nouveau = !is_file($csv);
if ($fh = @fopen($csv, 'a')) {
    if (flock($fh, LOCK_EX)) {
        if ($nouveau) {
            fwrite($fh, "\xEF\xBB\xBF"); // pour qu'Excel lise bien les accents
            fputcsv($fh, ['Reçue le', 'Nom', 'Société', 'E-mail', 'Téléphone', 'Prestation', 'Véhicule', 'Date', 'Heure', 'Départ', 'Destination', 'Message', 'E-mail envoyé', 'Statut'], ';');
        }
        $ligneCsv = array_merge([date('Y-m-d H:i')], array_values($d));
        // Neutralise les formules si le fichier est ouvert dans un tableur
        $ligneCsv = array_map(fn($c) => preg_match('/^(=|@|[+\-](?![0-9 ]))/', (string) $c) ? "'" . $c : $c, $ligneCsv);
        $positionLigne = ftell($fh);
        fputcsv($fh, array_merge($ligneCsv, ['en cours', 'Nouveau']), ';');
        flock($fh, LOCK_UN);
    }
    fclose($fh);
}

// 2. Envoi de l'e-mail
$sujet = 'Nouvelle demande de devis — ' . $d['nom'] . ($d['societe'] !== '' ? ' (' . $d['societe'] . ')' : '') . ' — ' . trim($d['depart'] . ' → ' . $d['destination']) . ($d['email'] === '' ? ' (répondre par WhatsApp)' : '');
$lignes = [
    'Client'        => $d['nom'],
    'Société'       => $d['societe'],
    'E-mail'        => $d['email'],
    'Téléphone'     => $d['telephone'],
    'Prestation'    => $d['prestation'],
    'Véhicule'      => $d['vehicule'],
    'Date et heure' => trim($d['date'] . ' ' . $d['heure']),
    'Départ'        => $d['depart'],
    'Destination'   => $d['destination'],
];
// Boutons de réponse : le chauffeur répond au client en un clic (WhatsApp, appel, e-mail)
$telIntl = $d['telephone'];
if (preg_match('/^0[1-9]\d{8}$/', $telIntl)) { $telIntl = '+41' . substr($telIntl, 1); } // numéro local : supposé suisse
$waNum = preg_replace('/\D/', '', $telIntl);
$trajet = trim($d['depart'] . ' → ' . $d['destination']);
$quandTxt = trim($d['date'] . ' ' . $d['heure']);
$texteWa = 'Bonjour ' . $d['nom'] . ', Prosper & Co. ici, suite à votre demande sur lux-taxi.com (' . $trajet . ', ' . $quandTxt . '). Le prix fixe est de … CHF, tout compris. Je vous confirme la réservation ?';
$btn = 'display:inline-block;margin:0 8px 8px 0;padding:12px 18px;border-radius:6px;text-decoration:none;font-weight:bold;';
$boutons = '';
if ($waNum !== '') {
    $boutons .= '<a href="https://wa.me/' . $waNum . '?text=' . rawurlencode($texteWa) . '" style="' . $btn . 'background:#25D366;color:#fff;">Répondre sur WhatsApp</a>';
    $boutons .= '<a href="tel:' . h($telIntl) . '" style="' . $btn . 'background:#111;color:#fff;">Appeler ' . h($d['telephone']) . '</a>';
}
if ($d['email'] !== '') {
    $corpsMail = "Bonjour " . $d['nom'] . ",\n\nMerci pour votre demande (" . $trajet . ", " . $quandTxt . ").\nLe prix fixe est de … CHF, tout compris.\n\nBien à vous,\nProsper & Co.";
    $boutons .= '<a href="mailto:' . h($d['email']) . '?subject=' . rawurlencode('Votre devis Prosper & Co. — ' . $trajet) . '&body=' . rawurlencode($corpsMail) . '" style="' . $btn . 'background:#c6a96b;color:#050506;">Répondre par e-mail</a>';
}
$html = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body style="font-family:Arial,Helvetica,sans-serif;color:#111;">';
$html .= '<h2 style="margin:0 0 12px;">Nouvelle demande de devis — lux-taxi.com</h2>';
$html .= '<p style="margin:0 0 8px;">' . $boutons . '</p>';
if ($d['email'] === '') {
    $html .= '<p style="background:#fff4e5;border-left:4px solid #e8a03c;padding:10px 12px;margin:0 0 16px;font-size:14px;">Le client n\'a pas laissé d\'e-mail : répondez par <strong>WhatsApp</strong> ou par <strong>téléphone</strong> (le bouton « Répondre » de votre messagerie écrirait à info@lux-taxi.com).</p>';
} else {
    $html .= '<p style="color:#555;margin:0 0 16px;font-size:14px;">Le bouton « Répondre » de votre messagerie écrit directement au client (' . h($d['email']) . ').</p>';
}
$html .= '<table cellpadding="6" style="border-collapse:collapse;">';
foreach ($lignes as $label => $val) {
    if ($val === '') { continue; }
    $html .= '<tr><td style="color:#666;border-bottom:1px solid #eee;">' . h($label) . '</td><td style="border-bottom:1px solid #eee;"><strong>' . h($val) . '</strong></td></tr>';
}
$html .= '</table>';
if ($d['message'] !== '') {
    $html .= '<p style="color:#666;margin:16px 0 4px;">Message</p><p style="background:#f5f5f5;padding:12px;">' . nl2br(h($d['message'])) . '</p>';
}
if (!empty($lien)) {
    $html .= '<p style="margin:16px 0;"><a href="' . h($lien) . '" style="' . $btn . 'background:#c6a96b;color:#050506;">Voir la position du client sur la carte</a></p>';
}
$html .= '</body></html>';

$entetes = [
    'MIME-Version: 1.0',
    'Content-Type: text/html; charset=utf-8',
    'From: ' . mb_encode_mimeheader('Lux Taxi — Site web', 'UTF-8') . ' <' . EXPEDITEUR . '>',
];
if ($d['email'] !== '') {
    $entetes[] = 'Reply-To: ' . mb_encode_mimeheader(preg_replace('/[^\p{L}\p{N} .\'-]/u', '', $d['nom']) ?: 'Client', 'UTF-8') . ' <' . $d['email'] . '>';
}
$envoye = @mail(DESTINATAIRE, mb_encode_mimeheader($sujet, 'UTF-8'), $html, implode("\r\n", $entetes), '-f' . EXPEDITEUR);

// Note l'état de l'envoi dans le fichier des demandes
if (is_file($csv) && isset($positionLigne)) {
    $contenu = (string) @file_get_contents($csv);
    $fin = substr($contenu, $positionLigne);
    $fin = preg_replace('/;"?en cours"?;Nouveau\s*$/u', ';' . ($envoye ? 'oui' : 'NON') . ';Nouveau' . "\n", $fin, 1);
    @file_put_contents($csv, substr($contenu, 0, $positionLigne) . $fin, LOCK_EX);
}

// 3. Réponse au visiteur
if ($envoye) {
    repondre(200, ['success' => true]);
}
repondre(500, [
    'success' => false,
    'error'   => 'Sending failed. Please message us on WhatsApp or call ' . TELEPHONE . '.',
]);
