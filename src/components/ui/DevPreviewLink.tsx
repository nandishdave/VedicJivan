// Local development only: with no queue/email configured the API runs the job
// in-process and returns a `preview_url` where the would-be email is rendered
// as a page. Deployed environments never send one, so this renders nothing.
export function DevPreviewLink({ url }: { url: string | null }) {
  if (!url) return null;
  return (
    <p className="mb-8 rounded-lg border border-dashed border-primary-400 px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
      Local dev — no email is sent.{" "}
      <a
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        className="font-medium text-primary-600 underline hover:text-primary-700"
      >
        Open the result in a new tab
      </a>
    </p>
  );
}
