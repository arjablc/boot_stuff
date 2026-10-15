package pokecache

import (
	"log"
	"sync"
	"time"
)

type Cache struct {
	caches map[string]CacheEntry
	mu     sync.Mutex
}

func (C *Cache) Add(key string, value []byte) {
	timestamp := time.Now()
	entry := CacheEntry{createdAt: timestamp, val: value}
	C.mu.Lock()
	defer C.mu.Unlock()
	C.caches[key] = entry
}
func (C *Cache) Get(key string) ([]byte, bool) {
	C.mu.Lock()
	defer C.mu.Unlock()
	value, exists := C.caches[key]
	if exists {
		log.Printf("cache hit: %s", key)
	} else {
		log.Printf("cache miss: %s", key)
	}
	return value.val, exists
}
func (C *Cache) reapLoop(interval time.Duration) {
	ticker := time.NewTicker(interval)
	for range ticker.C {
		C.mu.Lock()
		for key, entry := range C.caches {
			now := time.Now()
			if now.Sub(entry.createdAt) > interval {
				delete(C.caches, key)
			}
		}
		C.mu.Unlock()
	}
}

type CacheEntry struct {
	createdAt time.Time
	val       []byte
}

func NewCache(interval time.Duration) *Cache {
	cacheMap := make(map[string]CacheEntry)
	cache := Cache{
		caches: cacheMap,
	}
	go cache.reapLoop(interval)
	return &cache
}
