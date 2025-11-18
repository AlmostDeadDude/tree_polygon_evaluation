<?php

function tree_demo_random_key(): string
{
    try {
        return bin2hex(random_bytes(6));
    } catch (Exception $e) {
        return (string)round(microtime(true) * 1000);
    }
}

$Campaign_id = isset($_GET["campaign"]) && $_GET["campaign"] !== '' ? $_GET["campaign"] : "tree_demo_campaign";
$Worker_id = isset($_GET["worker"]) && $_GET["worker"] !== '' ? $_GET["worker"] : "guest_reviewer";
$Rand_key = isset($_GET["rand_key"]) && $_GET["rand_key"] !== '' ? $_GET["rand_key"] : tree_demo_random_key();
$proof_code = 'DEMO PROOF CODE';

$absoluteJobPaths = glob(__DIR__ . '/jobs/job_*.txt');

if (!$absoluteJobPaths) {
    @require_once('header.php');
    echo '<section class="info-block">
        <h2>No archived jobs found</h2>
        <p>The jobs directory is empty, so the Tree Polygon Evaluation demo cannot load any examples. Please add at least one job file to <code>web/jobs</code>.</p>
    </section>';
    @require_once('footer.php');
    exit();
}

$selectedJobPath = $absoluteJobPaths[array_rand($absoluteJobPaths)];
$jobFilename = basename($selectedJobPath);
$json_filename = 'jobs/' . $jobFilename;
preg_match('/job_(\d+)\.txt$/', $jobFilename, $jobNumberMatches);
$selectedJobNumber = isset($jobNumberMatches[1]) ? (int)$jobNumberMatches[1] : $jobFilename;

$handle = fopen($selectedJobPath, "r");
$data = [];
while (($line = fgets($handle)) !== false) {
    if (trim($line) === '') {
        continue;
    }

    $json_data = json_decode($line, true);
    if ($json_data === null) {
        continue;
    }

    $data[] = $json_data;
}
fclose($handle);

$bg_image_filename = 'pics/70.png';
$bg_image_info = getimagesize($bg_image_filename);
$bg_image_width = $bg_image_info[0];
$bg_image_height = $bg_image_info[1];

require_once('header.php');

echo '<section class="info-block hero">
    <h1>Tree Polygon Evaluation &mdash; Demo version</h1>
    <p>This read-only build mirrors the original crowdsourcing task: you receive a random archived assignment (currently job <strong>#' . htmlspecialchars((string)$selectedJobNumber) . '</strong>), review the polygons, and finish with a demo proof code that historically confirmed payment on the crowdsourcing platform.</p>
</section>';

if (empty($data)) {
    echo '<section class="info-block">
        <h2>No tasks found in this job</h2>
        <p>The randomly selected archive file did not contain any task definitions. Refresh the page to load a different job.</p>
    </section>';
}

foreach ($data as $index => $json_obj) {
    $points = $json_obj[0]['points'];
    $number_points = $json_obj[0]['number_points'];
    $ID = $json_obj[0]['ID'];
    if (empty($points)) {
        continue;
    }
    $canvas_width = $bg_image_width;
    $canvas_height = $bg_image_height;

    echo '<div class="task-wrapper" id="task_' . htmlspecialchars($ID) . '">';
    echo '<div class="canvas-wrapper">';
    echo '<h1>Task #' . htmlspecialchars($ID) . ': ' . htmlspecialchars($number_points) . ' corners</h1>';
    echo '<canvas id="canvas_' . $index . '" width="' . $canvas_width . '" height="' . $canvas_height . '" style="background-image:url(' . $bg_image_filename . ');border:1px solid black;"></canvas>';
    echo '<script>
        var canvas_' . $index . ' = document.getElementById("canvas_' . $index . '");
        var ctx_' . $index . ' = canvas_' . $index . '.getContext("2d");
        ctx_' . $index . '.fillStyle = "rgba(255,255,255,0.1)";
        ctx_' . $index . '.lineWidth = "5";
        ctx_' . $index . '.strokeStyle = "black";
        ';
    foreach ($points as $i => $point) {
        echo 'ctx_' . $index . '.beginPath();
        ctx_' . $index . '.arc(' . $point['x'] . ', ' . $point['y'] . ', 2, 0, 2 * Math.PI);
        ctx_' . $index . '.fill();
        ';
    }
    echo 'ctx_' . $index . '.beginPath();
        ctx_' . $index . '.moveTo(' . $points[0]['x'] . ', ' . $points[0]['y'] . ');
        ';
    for ($i = 1; $i < count($points); $i++) {
        echo 'ctx_' . $index . '.lineTo(' . $points[$i]['x'] . ', ' . $points[$i]['y'] . ');
        ';
    }
    echo 'ctx_' . $index . '.lineTo(' . $points[0]['x'] . ', ' . $points[0]['y'] . ');
        ctx_' . $index . '.stroke();
        ctx_' . $index . '.closePath();
    </script>';
    echo '</div>';
    echo '
    <div class="rating-wrapper">
      <h2>How well does this outline match the tree?</h2>
      <div class="rating-options">
          <div class="rating a" result-value="100">Very good</div>
          <div class="rating b" result-value="75">Good</div>
          <div class="rating c" result-value="50">Acceptable</div>
          <div class="rating d" result-value="25">Bad</div>
          <div class="rating e" result-value="0">Very bad</div>
      </div>
    </div>
  ';
    echo '</div>';
}

echo '<p class="demo-note">Rate every task to reveal the DEMO PROOF CODE that workers previously submitted on the crowdsourcing platform to receive payment.</p>';
echo '<button id="confirmBtn">Finish demo</button>';
echo '<div id="demoComplete" class="demo-complete" aria-live="polite"></div>';

$userInfo = [
    'campaign' => $Campaign_id,
    'worker' => $Worker_id,
    'proofCode' => $proof_code
];

$dataInfo = [
    'file' => $json_filename,
    'image' => $bg_image_filename,
    'job' => $selectedJobNumber,
    'iteration' => 'demo',
    'mode' => 'readonly'
];

echo '<script>';
echo 'const userInfo = ' . json_encode($userInfo, JSON_UNESCAPED_SLASHES) . ';';
echo 'const dataInfo = ' . json_encode($dataInfo, JSON_UNESCAPED_SLASHES) . ';';
echo '</script>';

require_once('footer.php');
