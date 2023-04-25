<?php
$firstTime = $_GET['firstTime'];
$Campaign_id = $_GET["campaign"];
$Worker_id = $_GET["worker"];
$Rand_key = $_GET["rand_key"];

@require_once('header.php');
echo '
<h2>Introduction</h2>
<p>Welcome to our tree outline evaluation task! In this task, you will be presented with a series of pictures that contain a tree, and your job is to evaluate how well the selection polygon matches the tree outline. There are five different color-coded categories to choose from: <span class="a pm-5">Very Good</span>, <span class="b pm-5">Good</span>, <span class="c pm-5">Acceptable</span>, <span class="d pm-5">Bad</span>, and <span class="e pm-5">Very Bad</span>. Your ratings will help us to improve the accuracy of our automatic tree selection algorithms in the future.</p>
<h2>Task Instructions</h2>
<p>To complete the task, simply click on the button with the appropriate option for each picture. After rating all provided pictures, submit your results and you will receive a unique VCODE to claim your payment. </p>
<p>It\'s important to evaluate the selection based on how well it matches the tree outline, and not based on any other factors. To help you with this, we have provided example pictures for each of the five categories, which you can refer to as a guide when evaluating the pictures.</p>
<h2>Examples</h2>
<h3>Here are some examples of what we mean by each of the five categories:</h3>
<ul>
  <li><strong class="a pm-5">Very Good:</strong> The selection perfectly matches the tree outline, with no parts of the tree left unselected, and no non-tree objects or surfaces included in the selection.
  <div style="width:100%; max-width: 845px; padding-left: 10px; display: flex;" class="a">
  <img src="pics/examples/exA.png" alt="Very Good" style="width:100%; max-width: 835px;">
  </div><br><br>
  </li>
  <li><strong class="b pm-5">Good:</strong> The selection mostly matches the tree outline, with only minor deviations or small parts of the tree left unselected or non-tree objects or surfaces included in the selection.
  <div style="width:100%; max-width: 845px; padding-left: 10px; display: flex;" class="b">
  <img src="pics/examples/exB.png" alt="Very Good" style="width:100%; max-width: 835px;">
  </div><br><br>
  </li>
  <li><strong class="c pm-5">Acceptable:</strong> The selection matches the general shape of the tree, but there are significant deviations or parts of the tree left unselected, or non-tree objects or surfaces included in the selection.
  <div style="width:100%; max-width: 845px; padding-left: 10px; display: flex;" class="c">
  <img src="pics/examples/exC.png" alt="Very Good" style="width:100%; max-width: 835px;">
  </div><br><br>
  </li>
  <li><strong class="d pm-5">Bad:</strong> The selection does not match the tree outline, with large parts of the tree left unselected or significant non-tree objects or surfaces included in the selection.
  <div style="width:100%; max-width: 845px; padding-left: 10px; display: flex;" class="d">
  <img src="pics/examples/exD.png" alt="Very Good" style="width:100%; max-width: 835px;">
  </div><br><br>
  </li>
  <li><strong class="e pm-5">Very Bad:</strong> The selection is completely unrelated to the tree outline, with almost no parts of the tree selected and significant non-tree objects or surfaces included in the selection.
  <div style="width:100%; max-width: 845px; padding-left: 10px; display: flex;" class="e">
  <img src="pics/examples/exE.png" alt="Very Good" style="width:100%; max-width: 835px;">
  </div>
  </li>
</ul>
<h2>Conclusion</h2>
<p>Thank you for helping with our research! Your contributions will help us to improve our automatic tree selection algorithms, which will have a wide range of applications in fields such as agriculture, forestry, and urban planning. We appreciate your time and effort, and wish you good luck with the task.</p>
';
if ($firstTime == 'true') {
    echo '<button class="toTaskBtn" onclick="startTask()">Start task</button>';
    echo '<script>
    function startTask() {
        window.location.href = "index.php?campaign=' . $Campaign_id . '&worker=' . $Worker_id . '&rand_key=' . $Rand_key . '";
    }
    </script>';
}
@require_once('footer.php');
