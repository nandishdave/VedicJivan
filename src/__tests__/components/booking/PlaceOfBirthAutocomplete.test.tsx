import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, fireEvent, cleanup, waitFor, act } from "@testing-library/react";
import { PlaceOfBirthAutocomplete } from "@/components/booking/PlaceOfBirthAutocomplete";

// Save original env
const originalEnv = { ...process.env };

function setupGoogleMock(options?: {
  predictions?: { place_id: string; description: string }[];
  placeDetails?: {
    lat: number;
    lng: number;
    name: string;
  };
}) {
  const predictions = options?.predictions ?? [];
  const details = options?.placeDetails;

  const mockGetPlacePredictions = vi.fn(
    (_req: unknown, callback: (preds: typeof predictions | null, status: string) => void) => {
      callback(predictions, predictions.length > 0 ? "OK" : "ZERO_RESULTS");
    }
  );

  const mockGetDetails = vi.fn(
    (_req: unknown, callback: (place: unknown, status: string) => void) => {
      if (details) {
        callback(
          {
            geometry: {
              location: { lat: () => details.lat, lng: () => details.lng },
            },
            formatted_address: details.name,
            name: details.name,
          },
          "OK"
        );
      }
    }
  );

  // Use real class constructors so `new` works
  class MockAutocompleteService {
    getPlacePredictions = mockGetPlacePredictions;
  }
  class MockPlacesService {
    getDetails = mockGetDetails;
  }
  class MockSessionToken {}

  Object.defineProperty(window, "google", {
    value: {
      maps: {
        places: {
          AutocompleteService: MockAutocompleteService,
          PlacesService: MockPlacesService,
          AutocompleteSessionToken: MockSessionToken,
          PlacesServiceStatus: { OK: "OK" },
        },
      },
    },
    writable: true,
    configurable: true,
  });

  return { mockGetPlacePredictions, mockGetDetails };
}

describe("PlaceOfBirthAutocomplete", () => {
  beforeEach(() => {
    cleanup();
    vi.clearAllMocks();
    vi.useFakeTimers({ shouldAdvanceTime: true });
    process.env = { ...originalEnv };
  });

  afterEach(() => {
    vi.useRealTimers();
    process.env = originalEnv;
  });

  it("disables input when no API key is configured", () => {
    delete process.env.NEXT_PUBLIC_GOOGLE_PLACES_API_KEY;
    render(<PlaceOfBirthAutocomplete value="" onPlaceSelect={vi.fn()} />);

    const input = screen.getByPlaceholderText("Google Places API key not configured");
    expect(input).toBeDisabled();
  });

  it("renders input with correct placeholder when API key is set", () => {
    process.env.NEXT_PUBLIC_GOOGLE_PLACES_API_KEY = "test-key";
    render(<PlaceOfBirthAutocomplete value="" onPlaceSelect={vi.fn()} />);
    expect(screen.getByPlaceholderText("Start typing a city name...")).toBeInTheDocument();
  });

  it("displays the provided value in the input", () => {
    process.env.NEXT_PUBLIC_GOOGLE_PLACES_API_KEY = "test-key";
    render(<PlaceOfBirthAutocomplete value="Mumbai, India" onPlaceSelect={vi.fn()} />);
    expect(screen.getByDisplayValue("Mumbai, India")).toBeInTheDocument();
  });

  it("updates input value on typing", () => {
    process.env.NEXT_PUBLIC_GOOGLE_PLACES_API_KEY = "test-key";
    render(<PlaceOfBirthAutocomplete value="" onPlaceSelect={vi.fn()} />);
    const input = screen.getByPlaceholderText("Start typing a city name...");
    fireEvent.change(input, { target: { value: "Del" } });
    expect(input).toHaveValue("Del");
  });

  it("shows suggestions dropdown when Google API returns predictions", async () => {
    process.env.NEXT_PUBLIC_GOOGLE_PLACES_API_KEY = "test-key";
    setupGoogleMock({
      predictions: [
        { place_id: "p1", description: "Delhi, India" },
        { place_id: "p2", description: "Denver, USA" },
      ],
    });

    render(<PlaceOfBirthAutocomplete value="" onPlaceSelect={vi.fn()} />);

    const input = screen.getByPlaceholderText("Start typing a city name...");
    fireEvent.change(input, { target: { value: "Del" } });

    act(() => {
      vi.advanceTimersByTime(350);
    });

    await waitFor(() => {
      expect(screen.getByText("Delhi, India")).toBeInTheDocument();
      expect(screen.getByText("Denver, USA")).toBeInTheDocument();
    });
  });

  it("calls onPlaceSelect when a suggestion is clicked", async () => {
    process.env.NEXT_PUBLIC_GOOGLE_PLACES_API_KEY = "test-key";
    const onPlaceSelect = vi.fn();

    setupGoogleMock({
      predictions: [{ place_id: "p1", description: "Delhi, India" }],
      placeDetails: { lat: 28.6139, lng: 77.209, name: "Delhi" },
    });

    render(<PlaceOfBirthAutocomplete value="" onPlaceSelect={onPlaceSelect} />);

    const input = screen.getByPlaceholderText("Start typing a city name...");
    fireEvent.change(input, { target: { value: "Del" } });

    act(() => {
      vi.advanceTimersByTime(350);
    });

    await waitFor(() => {
      expect(screen.getByText("Delhi, India")).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText("Delhi, India"));

    await waitFor(() => {
      expect(onPlaceSelect).toHaveBeenCalledWith({
        name: "Delhi, India",
        latitude: 28.6139,
        longitude: 77.209,
      });
    });
  });

  it("hides dropdown on click outside", async () => {
    process.env.NEXT_PUBLIC_GOOGLE_PLACES_API_KEY = "test-key";
    setupGoogleMock({
      predictions: [{ place_id: "p1", description: "Delhi, India" }],
    });

    render(<PlaceOfBirthAutocomplete value="" onPlaceSelect={vi.fn()} />);

    const input = screen.getByPlaceholderText("Start typing a city name...");
    fireEvent.change(input, { target: { value: "Del" } });

    act(() => {
      vi.advanceTimersByTime(350);
    });

    await waitFor(() => {
      expect(screen.getByText("Delhi, India")).toBeInTheDocument();
    });

    fireEvent.mouseDown(document.body);

    await waitFor(() => {
      expect(screen.queryByText("Delhi, India")).not.toBeInTheDocument();
    });
  });

  it("does not fetch predictions for input shorter than 2 characters", () => {
    process.env.NEXT_PUBLIC_GOOGLE_PLACES_API_KEY = "test-key";
    const { mockGetPlacePredictions } = setupGoogleMock();

    render(<PlaceOfBirthAutocomplete value="" onPlaceSelect={vi.fn()} />);

    const input = screen.getByPlaceholderText("Start typing a city name...");
    fireEvent.change(input, { target: { value: "D" } });

    act(() => {
      vi.advanceTimersByTime(350);
    });

    expect(mockGetPlacePredictions).not.toHaveBeenCalled();
  });
});
