"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { MapPin } from "lucide-react";

interface PlaceOfBirthAutocompleteProps {
  value: string;
  onPlaceSelect: (place: { name: string; latitude: number; longitude: number }) => void;
}

function useGooglePlaces() {
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const apiKey = process.env.NEXT_PUBLIC_GOOGLE_PLACES_API_KEY;
    if (!apiKey) return;

    if (window.google?.maps?.places) {
      setReady(true);
      return;
    }

    const existing = document.querySelector(
      'script[src*="maps.googleapis.com/maps/api/js"]'
    );
    if (existing) {
      existing.addEventListener("load", () => setReady(true));
      return;
    }

    const script = document.createElement("script");
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places`;
    script.async = true;
    script.onload = () => setReady(true);
    document.head.appendChild(script);
  }, []);

  return ready;
}

export function PlaceOfBirthAutocomplete({
  value,
  onPlaceSelect,
}: PlaceOfBirthAutocompleteProps) {
  const [inputValue, setInputValue] = useState(value);
  const [suggestions, setSuggestions] = useState<
    google.maps.places.AutocompletePrediction[]
  >([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const ready = useGooglePlaces();
  const autocompleteService =
    useRef<google.maps.places.AutocompleteService | null>(null);
  const placesService = useRef<google.maps.places.PlacesService | null>(null);
  const sessionToken =
    useRef<google.maps.places.AutocompleteSessionToken | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const dummyDiv = useRef<HTMLDivElement>(null);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    if (ready) {
      autocompleteService.current =
        new google.maps.places.AutocompleteService();
      if (dummyDiv.current) {
        placesService.current = new google.maps.places.PlacesService(
          dummyDiv.current
        );
      }
      sessionToken.current =
        new google.maps.places.AutocompleteSessionToken();
    }
  }, [ready]);

  // Sync external value
  useEffect(() => {
    setInputValue(value);
  }, [value]);

  // Click-outside handler
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (
        containerRef.current &&
        !containerRef.current.contains(e.target as Node)
      ) {
        setShowDropdown(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const fetchPredictions = useCallback(
    (text: string) => {
      if (!autocompleteService.current || text.length < 2) {
        setSuggestions([]);
        return;
      }

      autocompleteService.current.getPlacePredictions(
        {
          input: text,
          types: ["(cities)"],
          sessionToken: sessionToken.current || undefined,
        },
        (predictions, status) => {
          if (
            status === google.maps.places.PlacesServiceStatus.OK &&
            predictions
          ) {
            setSuggestions(predictions);
            setShowDropdown(true);
          } else {
            setSuggestions([]);
          }
        }
      );
    },
    []
  );

  const handleInputChange = (text: string) => {
    setInputValue(text);
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => fetchPredictions(text), 300);
  };

  const handleSelect = (
    prediction: google.maps.places.AutocompletePrediction
  ) => {
    if (!placesService.current) return;

    placesService.current.getDetails(
      {
        placeId: prediction.place_id,
        fields: ["geometry", "formatted_address", "name"],
        sessionToken: sessionToken.current || undefined,
      },
      (place, status) => {
        if (
          status === google.maps.places.PlacesServiceStatus.OK &&
          place?.geometry?.location
        ) {
          const name = prediction.description;
          const lat = place.geometry.location.lat();
          const lng = place.geometry.location.lng();
          setInputValue(name);
          setShowDropdown(false);
          setSuggestions([]);
          onPlaceSelect({ name, latitude: lat, longitude: lng });
          // Reset session token for next search
          sessionToken.current =
            new google.maps.places.AutocompleteSessionToken();
        }
      }
    );
  };

  const apiKey = process.env.NEXT_PUBLIC_GOOGLE_PLACES_API_KEY;

  return (
    <div ref={containerRef} className="relative">
      <div className="relative">
        <MapPin className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
        <input
          type="text"
          value={inputValue}
          onChange={(e) => handleInputChange(e.target.value)}
          onFocus={() => suggestions.length > 0 && setShowDropdown(true)}
          className="w-full rounded-lg border border-gray-300 py-2.5 pl-9 pr-4 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
          placeholder={
            apiKey
              ? "Start typing a city name..."
              : "Google Places API key not configured"
          }
          disabled={!apiKey}
        />
      </div>

      {/* Hidden div for PlacesService */}
      <div ref={dummyDiv} style={{ display: "none" }} />

      {/* Suggestions dropdown */}
      {showDropdown && suggestions.length > 0 && (
        <ul className="absolute z-50 mt-1 w-full rounded-lg border border-gray-200 bg-white shadow-lg max-h-60 overflow-y-auto">
          {suggestions.map((s) => (
            <li
              key={s.place_id}
              onClick={() => handleSelect(s)}
              className="flex items-center gap-2 px-3 py-2.5 text-sm cursor-pointer hover:bg-primary-50 transition-colors"
            >
              <MapPin className="h-4 w-4 flex-shrink-0 text-gray-400" />
              <span>{s.description}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
