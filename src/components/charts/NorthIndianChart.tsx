import { ABBR, PLANET_COLOR, type HouseData } from "@/lib/celebrities";

// North-Indian house polygons on a 0-4 grid (House 1 = top-centre diamond).
const POLY: Record<number, [number, number][]> = {
  1: [[2, 0], [3, 1], [2, 2], [1, 1]], 2: [[0, 0], [2, 0], [1, 1]], 3: [[0, 0], [1, 1], [0, 2]],
  4: [[0, 2], [1, 1], [2, 2], [1, 3]], 5: [[0, 2], [1, 3], [0, 4]], 6: [[0, 4], [1, 3], [2, 4]],
  7: [[2, 4], [1, 3], [2, 2], [3, 3]], 8: [[2, 4], [3, 3], [4, 4]], 9: [[4, 4], [3, 3], [4, 2]],
  10: [[4, 2], [3, 3], [2, 2], [3, 1]], 11: [[4, 2], [3, 1], [4, 0]], 12: [[4, 0], [3, 1], [2, 0]],
};
const S = 34;
const W = 4 * S;
const centroid = (pts: [number, number][]): [number, number] => [
  (pts.reduce((a, p) => a + p[0], 0) / pts.length) * S,
  (pts.reduce((a, p) => a + p[1], 0) / pts.length) * S,
];

export function NorthIndianChart({ data, title }: { data: HouseData; title: string }) {
  return (
    <div className="text-center">
      <div className="mb-1 text-sm font-bold text-primary-600">{title}</div>
      <svg viewBox={`0 0 ${W} ${W}`} className="mx-auto h-[150px] w-[150px]">
        <rect x={0} y={0} width={W} height={W} fill="#fff" stroke="#334155" strokeWidth={2} />
        <line x1={0} y1={0} x2={W} y2={W} stroke="#334155" />
        <line x1={W} y1={0} x2={0} y2={W} stroke="#334155" />
        <polygon
          points={`${2 * S},0 ${W},${2 * S} ${2 * S},${W} 0,${2 * S}`}
          fill="none"
          stroke="#334155"
        />
        {Array.from({ length: 12 }, (_, i) => i + 1).map((h) => {
          const [cx, cy] = centroid(POLY[h]);
          const planets = data.houses[h] ?? [];
          const chunks: string[][] = [];
          for (let i = 0; i < planets.length; i += 3) chunks.push(planets.slice(i, i + 3));
          return (
            <g key={h}>
              <text x={cx} y={cy - 8} fontSize={8} fill="#94a3b8" textAnchor="middle">
                {data.signByHouse[h]}
              </text>
              {chunks.map((chunk, li) => (
                <text
                  key={li}
                  x={cx}
                  y={cy + 4 + li * 11}
                  fontSize={9.5}
                  fontWeight={700}
                  textAnchor="middle"
                >
                  {chunk.map((p, j) => (
                    <tspan key={p} fill={PLANET_COLOR[p]}>
                      {ABBR[p]}
                      {j < chunk.length - 1 ? " " : ""}
                    </tspan>
                  ))}
                </text>
              ))}
            </g>
          );
        })}
      </svg>
    </div>
  );
}
