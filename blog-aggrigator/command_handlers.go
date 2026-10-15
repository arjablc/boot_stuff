package main

import (
	"context"
	"errors"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/arjablc/bloggrigator/internal/database"
	"github.com/google/uuid"
)

func handleLogin(s *state, cmd command) error {
	if len(cmd.args) != 1 {
		return errors.New("Login Handler got no args")
	}
	userName := cmd.args[0]
	user, err := s.db.GetUser(context.Background(), userName)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	fmt.Println(user)
	if err = s.cfg.SetUser(user.Name); err != nil {
		fmt.Println("Failed setting user ")
	}
	return nil

}

func handleRegister(s *state, cmd command) error {
	if len(cmd.args) != 1 {
		return errors.New("Register Handler got no args")
	}
	userName := cmd.args[0]
	createUserParms := database.CreateUserParams{ID: uuid.New(),
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
		Name:      userName,
	}
	user, err := s.db.CreateUser(context.Background(), createUserParms)
	if err := s.cfg.SetUser(user.Name); err != nil {
		fmt.Println("Failed writing name to the config file")
	}
	if err != nil {
		errstr := err.Error()
		fmt.Println(err)
		if strings.Contains(errstr, "duplicate") {
			os.Exit(1)
		}
	}
	fmt.Println("User has been set successfully")
	return nil

}

func handleReset(s *state, cmd command) error {
	err := s.db.ResetUsers(context.Background())
	if err != nil {
		fmt.Println(err)

	}
	fmt.Println("Users has been reset")
	return nil

}

func handleUsers(s *state, cmd command) error {
	users, err := s.db.GetUsers(context.Background())
	if err != nil {
		fmt.Println(err)
	}
	for _, user := range users {
		if user.Name == s.cfg.CurrentUsername {
			fmt.Printf("* %s (current)\n", user.Name)
		} else {
			fmt.Printf("* %s\n", user.Name)
		}
	}
	return nil

}

func handleAgg(s *state, cmd command) error {
	if len(cmd.args) < 1 {
		return errors.New("Invalid argument, pass on the time interval")

	}
	timeArgs := cmd.args[0]
	timeDuration, err := time.ParseDuration(timeArgs)
	if err != nil {
		return errors.New("Parsing time duration error. use durations like 1s, 1m, 1h")
	}
	fmt.Println("Starting scraping every [%s]", timeDuration)
	fmt.Println("Press CTRL+C to stop execution")
	ticker := time.NewTicker(timeDuration)
	for ; ; <-ticker.C {
		err := scrapeFeeds(s)
		if err != nil {
			return err
		}
	}
}

func handleAddFeed(s *state, cmd command, user database.User) error {
	if len(cmd.args) < 2 {
		return errors.New("Not enough arguments")
	}
	title, url := cmd.args[0], cmd.args[1]
	feedDto := database.CreatFeedParams{
		ID:        uuid.New(),
		Name:      title,
		Url:       url,
		UserID:    user.ID,
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
	}

	dbFeed, err := s.db.CreatFeed(context.Background(), feedDto)
	if err != nil {
		return err
	}

	feedFollowDto := database.CreateFeedFollowParams{
		ID:        uuid.New(),
		UserID:    user.ID,
		FeedID:    dbFeed.ID,
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
	}

	_, err = s.db.CreateFeedFollow(context.Background(), feedFollowDto)
	if err != nil {
		return err
	}
	fmt.Println(dbFeed)
	fmt.Printf("Following Feed %s by user %s", dbFeed.Name, user.Name)
	return nil

}

func handleFeeds(s *state, cmd command) error {
	rows, err := s.db.GetFeeds(context.Background())
	if err != nil {
		return err
	}
	fmt.Println("======================")
	for _, row := range rows {
		fmt.Printf("Title: %s, Url: %s\n", row.Name, row.Url)
		fmt.Printf("Added By: %s\n", row.Name_2)
		fmt.Println()
	}
	fmt.Println("======================")
	return nil

}

func handleFollow(s *state, cmd command, user database.User) error {
	if len(cmd.args) < 1 {
		err := errors.New("Not enough Args")
		return err
	}
	urlArg := cmd.args[0]

	feed, err := s.db.GetFeedByUrl(context.Background(), urlArg)
	if err != nil {
		return err
	}

	createFeedFollowDto := database.CreateFeedFollowParams{
		ID:        uuid.New(),
		UserID:    user.ID,
		FeedID:    feed.ID,
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
	}
	feedFollow, err := s.db.CreateFeedFollow(context.Background(), createFeedFollowDto)
	if err != nil {
		return err
	}
	fmt.Printf("Current user: %s,\nFollowed feed: %s", feedFollow.UserName, feedFollow.FeedName)
	return nil
}

func handleFollowing(s *state, cmd command, user database.User) error {
	feeds, err := s.db.GetFeedFollowsForUser(context.Background(), user.ID)
	if err != nil {
		return err
	}
	for _, feed := range feeds {
		fmt.Println(feed.Name)
	}
	return nil

}

func handleUnfollow(s *state, cmd command, user database.User) error {
	if len(cmd.args) < 1 {
		err := errors.New("Not enough Args")
		return err
	}
	urlArg := cmd.args[0]
	feed, err := s.db.GetFeedByUrl(context.Background(), urlArg)
	if err != nil {
		return err
	}
	err = s.db.DeleteFeedFollow(context.Background(), database.DeleteFeedFollowParams{
		FeedID: feed.ID,
		UserID: user.ID,
	})
	if err != nil {
		return err
	}
	fmt.Printf("Current user: %s,\nUnfolowed feed: %s", user.Name, feed.Name)
	return nil
}

func handleBrowse(s *state, cmd command) error {
	var limit int64 = 2
	if len(cmd.args) >= 1 {
		parsed, err := strconv.ParseInt(cmd.args[0], 10, 32)
		if err != nil {
			return errors.New("Invalid limit argument")
		}
		limit = parsed
	}

	posts, err := s.db.GetPostsForUser(context.Background(), int32(limit))
	if err != nil {
		return errors.New("Failed to get posts")
	}
	for _, post := range posts {
		fmt.Println("==================")
		fmt.Printf("Post:\n Title: %s,\n Description: %s,\n Link: %s,\n", post.Title, post.Description, post.Url)
		fmt.Println("==================")
	}
	return nil

}
