import { describe, it, expect, beforeEach } from "vitest";
import {
  getToken,
  getRefreshToken,
  setTokens,
  clearTokens,
  isAuthenticated,
} from "@/lib/auth";

describe("auth", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  describe("getToken", () => {
    it("returns null when no token is stored", () => {
      expect(getToken()).toBeNull();
    });

    it("returns the stored token", () => {
      localStorage.setItem("vj_token", "my-access-token");
      expect(getToken()).toBe("my-access-token");
    });
  });

  describe("getRefreshToken", () => {
    it("returns null when no refresh token is stored", () => {
      expect(getRefreshToken()).toBeNull();
    });

    it("returns the stored refresh token", () => {
      localStorage.setItem("vj_refresh", "my-refresh-token");
      expect(getRefreshToken()).toBe("my-refresh-token");
    });
  });

  describe("setTokens", () => {
    it("stores both access and refresh tokens", () => {
      setTokens("access-123", "refresh-456");
      expect(localStorage.getItem("vj_token")).toBe("access-123");
      expect(localStorage.getItem("vj_refresh")).toBe("refresh-456");
    });
  });

  describe("clearTokens", () => {
    it("removes both tokens from localStorage", () => {
      setTokens("a", "b");
      clearTokens();
      expect(localStorage.getItem("vj_token")).toBeNull();
      expect(localStorage.getItem("vj_refresh")).toBeNull();
    });
  });

  describe("isAuthenticated", () => {
    it("returns false when no token exists", () => {
      expect(isAuthenticated()).toBe(false);
    });

    it("returns true when a token exists", () => {
      setTokens("token", "refresh");
      expect(isAuthenticated()).toBe(true);
    });
  });
});
