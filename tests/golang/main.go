package main

import (
	"fmt"
	"net/http"
)

func DDos() error {
	req, err := http.Get("http://localhost:8080")
	if err != nil {
		return err
	}
	defer req.Body.Close()
	return nil
}

func main() {
	for i := 0; i < 100; i++ {
		if err := DDos(); err != nil {
			fmt.Printf("Error in request #%d: %v\n", i+1, err)
		}
	}
}
