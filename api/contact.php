<?php
/**
 * LT MAISON DE CHAUFFEURS • GENÈVE
 * Script de traitement sécurisé des demandes de devis et réservations
 * Optimisé pour hébergement Infomaniak (PHP 7.4 / 8.x)
 */

header('Content-Type: application/json; charset=utf-8');

// Autoriser uniquement les requêtes POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Méthode non autorisée.']);
    exit;
}

// Récupération des données POST (form-data ou json)
$inputJSON = file_get_contents('php://input');
$input = json_decode($inputJSON, true) ?: $_POST;

// Protection Anti-Spam (Honeypot)
if (!empty($input['website_check'])) {
    echo json_encode(['success' => true]);
    exit;
}

// Nettoyage et sécurisation des champs
$name = isset($input['name']) ? trim(strip_tags($input['name'])) : '';
$company = isset($input['company']) ? trim(strip_tags($input['company'])) : '';
$email = isset($input['email']) ? filter_var(trim($input['email']), FILTER_VALIDATE_EMAIL) : '';
$phone = isset($input['phone']) ? trim(strip_tags($input['phone'])) : '';
$service = isset($input['service']) ? trim(strip_tags($input['service'])) : 'Non spécifié';
$fleet = isset($input['fleet']) ? trim(strip_tags($input['fleet'])) : 'Non spécifié';
$date = isset($input['date']) ? trim(strip_tags($input['date'])) : 'À convenir';
$time = isset($input['time']) ? trim(strip_tags($input['time'])) : 'À convenir';
$pickup = isset($input['pickup']) ? trim(strip_tags($input['pickup'])) : 'Non spécifié';
$dropoff = isset($input['dropoff']) ? trim(strip_tags($input['dropoff'])) : 'Non spécifié';
$message = isset($input['message']) ? trim(strip_tags($input['message'])) : 'Aucune précision';

// Validation minimale
if (empty($name) || empty($phone) || !$email) {
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'error' => 'Veuillez renseigner votre nom, un email valide et votre numéro de téléphone.'
    ]);
    exit;
}

// Configuration de destination
$to = 'info@lux-taxi.com';
$subject = "Demande de Devis Chauffeur VIP — " . $name . (!empty($company) ? " (" . $company . ")" : "");

// Construction du corps du message HTML
$bodyHtml = "
<!DOCTYPE html>
<html>
<head>
  <meta charset='utf-8'>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #0b0b0c; color: #f5f1e8; padding: 20px; }
    .card { max-width: 600px; margin: 0 auto; background: #161619; border: 1px solid #C6A96B; border-radius: 16px; padding: 30px; }
    .header { border-bottom: 1px solid #292929; padding-bottom: 20px; margin-bottom: 20px; text-align: center; }
    .gold { color: #C6A96B; font-weight: bold; }
    .row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #222; font-size: 14px; }
    .label { color: #aaa59b; text-transform: uppercase; font-size: 11px; letter-spacing: 0.1em; }
    .val { color: #fff; font-weight: 500; text-align: right; }
    .msg-box { margin-top: 20px; background: #0b0b0c; padding: 15px; border-radius: 8px; border-left: 3px solid #C6A96B; font-size: 14px; color: #ddd; line-height: 1.5; }
    .footer { margin-top: 25px; text-align: center; font-size: 11px; color: #777; }
  </style>
</head>
<body>
  <div class='card'>
    <div class='header'>
      <div class='gold' style='font-size: 18px; letter-spacing: 0.15em;'>LT MAISON DE CHAUFFEURS • GENÈVE</div>
      <div style='font-size: 12px; color: #aaa59b; margin-top: 4px;'>Nouvelle Demande de Liaison Confidentielle</div>
    </div>

    <div class='row'><span class='label'>Client :</span><span class='val'>{$name}</span></div>
    " . (!empty($company) ? "<div class='row'><span class='label'>Société :</span><span class='val'>{$company}</span></div>" : "") . "
    <div class='row'><span class='label'>Email :</span><span class='val'><a href='mailto:{$email}' style='color:#C6A96B;'>{$email}</a></span></div>
    <div class='row'><span class='label'>Téléphone / WhatsApp :</span><span class='val'><a href='tel:{$phone}' style='color:#C6A96B;'>{$phone}</a></span></div>
    <div class='row'><span class='label'>Prestation :</span><span class='val'>{$service}</span></div>
    <div class='row'><span class='label'>Véhicule :</span><span class='val'>{$fleet}</span></div>
    <div class='row'><span class='label'>Date & Heure :</span><span class='val'>{$date} à {$time}</span></div>
    <div class='row'><span class='label'>Prise en charge :</span><span class='val'>{$pickup}</span></div>
    <div class='row'><span class='label'>Destination :</span><span class='val'>{$dropoff}</span></div>

    <div class='label' style='margin-top: 20px;'>Précisions & Consignes :</div>
    <div class='msg-box'>" . nl2br(htmlspecialchars($message)) . "</div>

    <div class='footer'>
      Ce message a été généré depuis le formulaire officiel de lux-taxi.com
    </div>
  </div>
</body>
</html>
";

// En-têtes pour envoi HTML propre
$headers = [];
$headers[] = 'MIME-Version: 1.0';
$headers[] = 'Content-type: text/html; charset=utf-8';
$headers[] = 'From: LT Conciergerie <no-reply@lux-taxi.com>';
$headers[] = 'Reply-To: ' . $name . ' <' . $email . '>';
$headers[] = 'X-Mailer: PHP/' . phpversion();

// Envoi via mail() natif Infomaniak
$sent = @mail($to, $subject, $bodyHtml, implode("\r\n", $headers));

if ($sent) {
    echo json_encode([
        'success' => true,
        'message' => 'Votre demande a été transmise avec succès à notre permanence.'
    ]);
} else {
    echo json_encode([
        'success' => false,
        'fallback' => true,
        'error' => "Serveur local ou sendmail non configuré."
    ]);
}
