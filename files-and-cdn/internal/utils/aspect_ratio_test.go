package utils

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestAspectRatioClassification(t *testing.T) {
	verticalVideo := "/home/knot/dev/boots/files-and-cdn/samples/boots-video-vertical.mp4"
	horizontalVideo := "/home/knot/dev/boots/files-and-cdn/samples/boots-video-horizontal.mp4"

	as, err := GetVideoAspectRatio(verticalVideo)
	require.NoError(t, err)
	assert.Equal(t, "9:16", as)

	as, err = GetVideoAspectRatio(horizontalVideo)
	require.NoError(t, err)
	assert.Equal(t, "16:9", as)
}
