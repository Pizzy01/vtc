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
    repondre(429, ['success' => false, 'error' => 'Trop de demandes en peu de temps. Merci de nous contacter sur WhatsApp ou au ' . TELEPHONE . '.']);
}
$historique[] = $maintenant;
@file_put_contents($fichierLimite, implode("\n", $historique), LOCK_EX);

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

if ($d['nom'] === '' || $d['telephone'] === '' || $d['email'] === '') {
    repondre(400, ['success' => false, 'error' => 'Merci d\'indiquer votre nom, un e-mail valide et votre téléphone.']);
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
$sujet = 'Nouvelle demande de devis — ' . $d['nom'] . ($d['societe'] !== '' ? ' (' . $d['societe'] . ')' : '');
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
$html = '<!DOCTYPE html><html><head><meta charset="utf-8"></head><body style="font-family:Arial,Helvetica,sans-serif;color:#111;">';
$html .= '<h2 style="margin:0 0 12px;">Nouvelle demande de devis — lux-taxi.com</h2><table cellpadding="6" style="border-collapse:collapse;">';
foreach ($lignes as $label => $val) {
    if ($val === '') { continue; }
    $html .= '<tr><td style="color:#666;border-bottom:1px solid #eee;">' . h($label) . '</td><td style="border-bottom:1px solid #eee;"><strong>' . h($val) . '</strong></td></tr>';
}
$html .= '</table>';
if ($d['message'] !== '') {
    $html .= '<p style="color:#666;margin:16px 0 4px;">Message</p><p style="background:#f5f5f5;padding:12px;">' . nl2br(h($d['message'])) . '</p>';
}
$html .= '<p style="color:#888;font-size:12px;margin-top:20px;">Répondez directement à cet e-mail pour écrire au client. WhatsApp / téléphone du client : ' . h($d['telephone']) . '</p></body></html>';

$entetes = [
    'MIME-Version: 1.0',
    'Content-Type: text/html; charset=utf-8',
    'From: ' . mb_encode_mimeheader('Lux Taxi — Site web', 'UTF-8') . ' <' . EXPEDITEUR . '>',
    'Reply-To: ' . mb_encode_mimeheader(preg_replace('/[^\p{L}\p{N} .\'-]/u', '', $d['nom']) ?: 'Client', 'UTF-8') . ' <' . $d['email'] . '>',
];
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
    'error'   => 'Votre demande n\'a pas pu être envoyée. Contactez-nous directement sur WhatsApp ou au ' . TELEPHONE . '.',
]);
