<?php
header('Content-Type: application/json');

$data = file_get_contents('php://input');

if (!$data) {
    echo json_encode([
        'status' => 'demo',
        'message' => 'Tree Polygon Evaluation now runs as a read-only demo. No payload received.',
        'proofCode' => 'DEMO PROOF CODE'
    ]);
    exit;
}

$json = json_decode($data);

if ($json === null) {
    echo json_encode([
        'status' => 'error',
        'message' => 'Invalid JSON payload.',
        'proofCode' => 'DEMO PROOF CODE'
    ]);
    exit;
}

$proofCode = 'DEMO PROOF CODE';
if (isset($json->userInfo->proofCode) && $json->userInfo->proofCode !== '') {
    $proofCode = $json->userInfo->proofCode;
}

echo json_encode([
    'status' => 'demo',
    'message' => 'Demo mode active: ratings stay in the browser, but you can still view historical aggregated results. Workers once used this proof code to confirm completion on the crowdsourcing platform.',
    'proofCode' => $proofCode
]);
