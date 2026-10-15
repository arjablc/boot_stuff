-- name: CreatFeed :one
INSERT INTO feeds (id, name,  url, user_id, created_at, updated_at, last_fetched_at)
VALUES (
    $1,
    $2,
    $3,
    $4,
    $5,
    $6,
    $7
)
RETURNING *;

-- name: GetFeedByUrl :one
SELECT * FROM feeds WHERE url=$1;

-- name: GetFeeds :many 
SELECT * FROM feeds inner join users on feeds.user_id = users.id;

-- name: MarkFeedFetched :exec
UPDATE feeds 
  SET  last_fetched_at = $2,
updated_at = $3
  WHERE id = $1;


-- name: GetNextFeedToFetch :one
SELECT * FROM feeds ORDER BY last_fetched_at ASC NULLS FIRST LIMIT 1;
