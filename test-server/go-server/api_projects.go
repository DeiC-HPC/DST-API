/*
 * Danish Data Portal - HPC API
 *
 * A Web API for HPC centers to communicate with the Danish Data Portal to manage access and data transfers
 *
 * API version: v1
 * Generated by: Swagger Codegen (https://github.com/swagger-api/swagger-codegen.git)
 */
package swagger

import (
	"net/http"
	"strings"
)

func ProjectsProjectNumberConfirmPost(w http.ResponseWriter, r *http.Request) {
	split1 := strings.Split(r.RequestURI, "/confirm")[0]
	projectNumber := strings.Split(split1, "/projects/")[1]
	updateMessageQueue(generateCreateProject(projectNumber))
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusOK)
}
