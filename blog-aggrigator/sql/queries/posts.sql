-- name: CreatePost :one 
INSERT INTO posts (id, title, url, description, published_at, feed_id,  created_at, updated_at)
VALUES (
    $1,
    $2,
    $3,
    $4,
    $5, 
    $6, 
    $7,
    $8
  
)
RETURNING *;

-- name: GetPostsForUser :many
SELECT * FROM posts ORDER BY published_at ASC LIMIT $1;



