
 NOTE: This will read the file to exhaustion
``` go 
 fileData, err := io.ReadAll(file)
```
Now you can't do 
```go  
n, err := io.Copy(dest, file)
```
leading to zero bytes being copied when using io.copy



