package api

import (
	"context"
	"encoding/xml"
	"html"
	"io"
	"log"
	"net/http"
)

type RSSFeed struct {
	Channel struct {
		Title       string    `xml:"title"`
		Link        string    `xml:"link"`
		Description string    `xml:"description"`
		Item        []RSSItem `xml:"item"`
	} `xml:"channel"`
}

type RSSItem struct {
	Title       string `xml:"title"`
	Link        string `xml:"link"`
	Description string `xml:"description"`
	PubDate     string `xml:"pubDate"`
}

func FetchFeed(ctx context.Context, feedUrl string) (*RSSFeed, error) {

	client := &http.Client{}

	fetchReq, err := http.NewRequestWithContext(ctx, "GET", feedUrl, nil)
	if err != nil {
		return nil, err
	}
	fetchReq.Header.Set("User-Agend", "gator")
	resp, err := client.Do(fetchReq)
	if err != nil {
		return nil, err
	}
	body, err := io.ReadAll(resp.Body)
	defer resp.Body.Close()

	var feed RSSFeed

	if err = xml.Unmarshal(body, &feed); err != nil {
		log.Fatalf("Failed to unmarshal")
	}

	sanitizeFeed(&feed)

	return &feed, nil

}

func sanitizeFeed(feed *RSSFeed) {
	feed.Channel.Title = html.UnescapeString(feed.Channel.Title)
	feed.Channel.Description = html.UnescapeString(feed.Channel.Description)
	for i, item := range feed.Channel.Item {
		feed.Channel.Item[i].Title = html.UnescapeString(item.Title)
		feed.Channel.Item[i].Description = html.UnescapeString(item.Description)
	}
}
