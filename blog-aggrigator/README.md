# BlogAggregator(Gator)
## Requirements
1. Postgres
2. SQLC
3. Goose
4. Go


## Usage


Clone the Repo
```

git clone https://github.com/arjablc/blog-aggrigator.git

```

CD into project
``` 
cd blog-aggrigator
```

Install 

``` 
go install .
```

Setup config file
1. create a file in home directory call it `.gatorconfig.json`
2. write the config
sample:
```json 
{
"db_url": "postgres://<user_name>:<password>@localhost:port/gator?sslmode=disable"
}
```

Database setup
- A database named `gator` should do

## CLI Commands

Run commands with the installed binary:

```sh
bloggrigator <command> [args...]
```

Or from the project directory:

```sh
go run . <command> [args...]
```

| Command | Args | Example |
|---|---|---|
| `login` | `<username>` | `bloggrigator login alice` |
| `register` | `<username>` | `bloggrigator register alice` |
| `reset` | none | `bloggrigator reset` |
| `users` | none | `bloggrigator users` |
| `agg` | `<interval>` | `bloggrigator agg 1m` |
| `addfeed` | `<title> <url>` | `bloggrigator addfeed "Go Blog" https://go.dev/blog/feed.atom` |
| `feeds` | none | `bloggrigator feeds` |
| `browse` | `[limit]` | `bloggrigator browse 10` |
| `follow` | `<feed_url>` | `bloggrigator follow https://go.dev/blog/feed.atom` |
| `following` | none | `bloggrigator following` |
| `unfollow` | `<feed_url>` | `bloggrigator unfollow https://go.dev/blog/feed.atom` |

Notes:
- `agg` accepts Go duration strings like `1s`, `30s`, `1m`, or `1h`.
- `browse` defaults to `2` posts when no limit is provided.
- `addfeed`, `follow`, `following`, and `unfollow` require a current logged-in user in `~/.gatorconfig.json`.
- This CLI does not currently include a built-in `help` command.







