## Strange PDF

We were given a PDF file containing some rotated `SharifCTF` string in the middle of page; Opening the file in a text editor shows there's 34 additional objects that were never referenced in the `PDF` file; I changed line 27 to `/Contents 7 0 R` and the secret revealed, so I wrote a script to generate the sequence of missing objects; Here's an example:


```
101 0 obj
<<
/Type /Page
/Parent 2 0 R
/Resources <<
    /XObject  <<
        /A 6 0 R
    >>
>>
/Contents 7 0 R
>>
endobj
```

It fetches the content of object `7` so we need 34 more objects to get all parts, also we need to increase `/Count` to `34` and add additional objects to `/Kids` in object number `2`:


```
2 0 obj
<<
  /Type /Pages
  /MediaBox [ 0 0 500 800 ]
  /Count 34
  /Kids [ 101 0 R 102 0 R 103 0 R 104 0 R 105 0 R 106 0 R 107 0 R 108 0 R 109 0 R 110 0 R 111 0 R 112 0 R 113 0 R 114 0 R 115 0 R 116 0 R 117 0 R 118 0 R 119 0 R 120 0 R 121 0 R 122 0 R 123 0 R 124 0 R 125 0 R 126 0 R 127 0 R 128 0 R 129 0 R 130 0 R 131 0 R 132 0 R 133 0 R  134 0 R
 ]
>>
endobj
```

After fixing the missing parts, we have a series of decimal codes; Converted them and got another flag:


```
123 100 49 50 52 50 100 50 100 48 57 54 57 54 51 55 52 49 100 100 101 55 101 100 55 57 99 51 99 52 48 57 99 52 54 125
```

