package main

import (
	"context"
	"database/sql"
	"fmt"
	"time"

	"github.com/arjablc/bloggrigator/internal/api"
	"github.com/arjablc/bloggrigator/internal/database"
	"github.com/google/uuid"
)

func toNullString(s string) sql.NullString {
	if s == "" {
		return sql.NullString{Valid: false}
	}
	return sql.NullString{String: s, Valid: true}
}

func scrapeFeeds(s *state) error {
	feed, err := s.db.GetNextFeedToFetch(context.Background())
	if err != nil {
		return err
	}
	fmt.Println("==========scraping=========")
	fmt.Printf("==========url:%s=========\n", feed.Url)
	fetchMarkParams := database.MarkFeedFetchedParams{ID: feed.ID, UpdatedAt: time.Now(), LastFetchedAt: sql.NullTime{Time: time.Now()}}
	err = s.db.MarkFeedFetched(context.Background(), fetchMarkParams)
	if err != nil {
		return err
	}
	rssFeed, err := api.FetchFeed(context.Background(), feed.Url)
	if err != nil {
		return err
	}
	for _, item := range rssFeed.Channel.Item {
		fmt.Printf("Saving %s\n", item.Title)
		parsedPubTime, err := time.Parse("Mon, 02 Jan 2006 15:04:05 -0700", item.PubDate)
		if err != nil {
			fmt.Println("Error occured during pub time parsing")
			fmt.Println(err)
			fmt.Println("Continuing anyways!!!")
		}
		savePostDto := database.CreatePostParams{
			ID:          uuid.New(),
			Title:       toNullString(item.Title),
			Description: toNullString(item.Description),
			Url:         item.Link,
			FeedID:      feed.ID,
			UpdatedAt:   time.Now(),
			CreatedAt:   time.Now(),
			PublishedAt: parsedPubTime,
		}
		_, err = s.db.CreatePost(context.Background(), savePostDto)
		if err != nil {
			fmt.Println("Error when inserting post")
			fmt.Println(err)
			fmt.Println("Continuing anyways!!!")
		}
	}
	return nil
}
