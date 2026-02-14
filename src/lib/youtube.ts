export interface YouTubeVideo {
  id: string;
  title: string;
  thumbnail: string;
  publishedAt: string;
  isShort: boolean;
}

const YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3";

export async function fetchChannelVideos(
  apiKey: string,
  channelId: string
): Promise<{ videos: YouTubeVideo[]; shorts: YouTubeVideo[] }> {
  // Step 1: Search for recent videos from channel
  const searchUrl = `${YOUTUBE_API_BASE}/search?part=snippet&channelId=${channelId}&order=date&type=video&maxResults=30&key=${apiKey}`;
  const searchRes = await fetch(searchUrl);

  if (!searchRes.ok) {
    throw new Error(`YouTube search API error: ${searchRes.status}`);
  }

  const searchData = await searchRes.json();
  const videoIds = searchData.items
    .map((item: { id: { videoId: string } }) => item.id.videoId)
    .join(",");

  if (!videoIds) {
    return { videos: [], shorts: [] };
  }

  // Step 2: Get video details (duration) to distinguish shorts from regular videos
  const detailsUrl = `${YOUTUBE_API_BASE}/videos?part=contentDetails,snippet&id=${videoIds}&key=${apiKey}`;
  const detailsRes = await fetch(detailsUrl);

  if (!detailsRes.ok) {
    throw new Error(`YouTube videos API error: ${detailsRes.status}`);
  }

  const detailsData = await detailsRes.json();

  const allVideos: YouTubeVideo[] = detailsData.items.map(
    (item: {
      id: string;
      snippet: { title: string; thumbnails: { high: { url: string } }; publishedAt: string };
      contentDetails: { duration: string };
    }) => {
      const durationSeconds = parseDuration(item.contentDetails.duration);
      return {
        id: item.id,
        title: item.snippet.title,
        thumbnail: item.snippet.thumbnails.high.url,
        publishedAt: item.snippet.publishedAt,
        isShort: durationSeconds <= 60,
      };
    }
  );

  const videos = allVideos.filter((v) => !v.isShort);
  const shorts = allVideos.filter((v) => v.isShort);

  return { videos, shorts };
}

// Parse ISO 8601 duration (PT1M30S, PT45S, PT1H2M3S) to seconds
function parseDuration(duration: string): number {
  const match = duration.match(/PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?/);
  if (!match) return 0;
  const hours = parseInt(match[1] || "0", 10);
  const minutes = parseInt(match[2] || "0", 10);
  const seconds = parseInt(match[3] || "0", 10);
  return hours * 3600 + minutes * 60 + seconds;
}
