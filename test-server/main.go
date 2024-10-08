/*
 * Danish Data Portal - HPC API
 *
 * A Web API for HPC centers to communicate with the Danish Data Portal to manage access and data transfers
 *
 * API version: v1
 * Generated by: Swagger Codegen (https://github.com/swagger-api/swagger-codegen.git)
 */
package main

import (
	"log"
	"net/http"
	sw "test-server/go-server"
)

func main() {
	log.Printf("Server started")

	router := sw.NewRouter()

	log.Fatal(http.ListenAndServe(":8080", router))
}
