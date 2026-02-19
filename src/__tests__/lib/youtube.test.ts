import { describe, it, expect, vi, beforeEach } from "vitest";
import { fetchChannelVideos } from "@/lib/youtube";

describe("fetchChannelVideos", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  const mockSearchResponse = (videoIds: string[]) => ({
    items: videoIds.map((id) => ({ id: { videoId: id } })),
  });

  const mockDetailsResponse = (
    videos: { id: string; title: string; duration: string }[]
  ) => ({
    items: videos.map((v) => ({
      id: v.id,
      snippet: {
        title: v.title,
        thumbnails: { high: { url: `https://img.youtube.com/${v.id}` } },
        publishedAt: "2026-01-01T00:00:00Z",
      },
      contentDetails: { duration: v.duration },
    })),
  });

  it("returns videos and shorts separated by duration", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockSearchResponse(["v1", "v2", "v3"])),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: () =>
          Promise.resolve(
            mockDetailsResponse([
              { id: "v1", title: "Long Video", duration: "PT5M30S" },
              { id: "v2", title: "Short Clip", duration: "PT45S" },
              { id: "v3", title: "Another Long", duration: "PT1H2M3S" },
            ])
          ),
      });
    vi.stubGlobal("fetch", fetchMock);

    const result = await fetchChannelVideos("key", "channel123");

    expect(result.videos).toHaveLength(2);
    expect(result.shorts).toHaveLength(1);
    expect(result.shorts[0].title).toBe("Short Clip");
    expect(result.videos[0].title).toBe("Long Video");
  });

  it("classifies 60-second video as short", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockSearchResponse(["v1"])),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: () =>
          Promise.resolve(
            mockDetailsResponse([
              { id: "v1", title: "Exactly 60s", duration: "PT1M" },
            ])
          ),
      });
    vi.stubGlobal("fetch", fetchMock);

    const result = await fetchChannelVideos("key", "ch");
    expect(result.shorts).toHaveLength(1);
    expect(result.videos).toHaveLength(0);
  });

  it("classifies 61-second video as regular", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockSearchResponse(["v1"])),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: () =>
          Promise.resolve(
            mockDetailsResponse([
              { id: "v1", title: "61 seconds", duration: "PT1M1S" },
            ])
          ),
      });
    vi.stubGlobal("fetch", fetchMock);

    const result = await fetchChannelVideos("key", "ch");
    expect(result.shorts).toHaveLength(0);
    expect(result.videos).toHaveLength(1);
  });

  it("returns empty arrays when no videos found", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ items: [] }),
    });
    vi.stubGlobal("fetch", fetchMock);

    const result = await fetchChannelVideos("key", "ch");
    expect(result.videos).toEqual([]);
    expect(result.shorts).toEqual([]);
  });

  it("throws on search API error", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce({
      ok: false,
      status: 403,
    });
    vi.stubGlobal("fetch", fetchMock);

    await expect(fetchChannelVideos("key", "ch")).rejects.toThrow(
      "YouTube search API error: 403"
    );
  });

  it("throws on details API error", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockSearchResponse(["v1"])),
      })
      .mockResolvedValueOnce({
        ok: false,
        status: 500,
      });
    vi.stubGlobal("fetch", fetchMock);

    await expect(fetchChannelVideos("key", "ch")).rejects.toThrow(
      "YouTube videos API error: 500"
    );
  });

  it("constructs correct search URL", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ items: [] }),
    });
    vi.stubGlobal("fetch", fetchMock);

    await fetchChannelVideos("my-api-key", "UCxyz");

    expect(fetchMock).toHaveBeenCalledWith(
      expect.stringContaining("channelId=UCxyz")
    );
    expect(fetchMock).toHaveBeenCalledWith(
      expect.stringContaining("key=my-api-key")
    );
  });

  it("sets isShort flag correctly on returned videos", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockSearchResponse(["v1"])),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: () =>
          Promise.resolve(
            mockDetailsResponse([
              { id: "v1", title: "Short", duration: "PT30S" },
            ])
          ),
      });
    vi.stubGlobal("fetch", fetchMock);

    const result = await fetchChannelVideos("key", "ch");
    expect(result.shorts[0].isShort).toBe(true);
  });

  it("parses hours-only duration correctly", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockSearchResponse(["v1"])),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: () =>
          Promise.resolve(
            mockDetailsResponse([
              { id: "v1", title: "Long", duration: "PT2H" },
            ])
          ),
      });
    vi.stubGlobal("fetch", fetchMock);

    const result = await fetchChannelVideos("key", "ch");
    expect(result.videos).toHaveLength(1);
    expect(result.shorts).toHaveLength(0);
  });

  it("includes thumbnail URL from API response", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockSearchResponse(["v1"])),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: () =>
          Promise.resolve(
            mockDetailsResponse([
              { id: "v1", title: "Video", duration: "PT5M" },
            ])
          ),
      });
    vi.stubGlobal("fetch", fetchMock);

    const result = await fetchChannelVideos("key", "ch");
    expect(result.videos[0].thumbnail).toBe("https://img.youtube.com/v1");
  });

  it("handles seconds-only duration", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockSearchResponse(["v1"])),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: () =>
          Promise.resolve(
            mockDetailsResponse([
              { id: "v1", title: "Tiny", duration: "PT15S" },
            ])
          ),
      });
    vi.stubGlobal("fetch", fetchMock);

    const result = await fetchChannelVideos("key", "ch");
    expect(result.shorts).toHaveLength(1);
  });
});
