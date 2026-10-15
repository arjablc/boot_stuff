package main

import (
	"database/sql"
	"fmt"
	"os"

	"github.com/arjablc/bloggrigator/internal/config"
	"github.com/arjablc/bloggrigator/internal/database"

	_ "github.com/lib/pq"
)

type state struct {
	db  *database.Queries
	cfg *config.Config
}

func main() {
	conf, err := config.Read()
	if err != nil {
		fmt.Println(err)
	}
	db, err := sql.Open("postgres", conf.DbUrl)
	if err != nil {
		fmt.Println("Db Open failed")
		os.Exit(1)
	}
	dbQueries := database.New(db)

	appState := state{cfg: conf, db: dbQueries}
	cmdsMap := make(map[string]func(*state, command) error)
	cmds := commands{cmds: cmdsMap}
	cmds.register("login", handleLogin)
	cmds.register("register", handleRegister)
	cmds.register("reset", handleReset)
	cmds.register("users", handleUsers)
	cmds.register("agg", handleAgg)
	cmds.register("addfeed", middlewareLoggedIn(handleAddFeed))
	cmds.register("feeds", handleFeeds)
	cmds.register("browse", handleBrowse)
	cmds.register("follow", middlewareLoggedIn(handleFollow))
	cmds.register("following", middlewareLoggedIn(handleFollowing))
	cmds.register("unfollow", middlewareLoggedIn(handleUnfollow))
	appArgs := os.Args
	if len(appArgs) < 2 {
		fmt.Println("Error: invalid arguments ")
		os.Exit(1)
	}
	cmd := command{cmd: appArgs[1], args: appArgs[2:]}
	err = cmds.run(&appState, cmd)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
