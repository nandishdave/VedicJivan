"use client";

import CountUp from "react-countup";
import { useInView } from "react-intersection-observer";

interface AnimatedCounterProps {
  end: number;
  suffix?: string;
  prefix?: string;
  duration?: number;
}

function AnimatedCounter({
  end,
  suffix = "",
  prefix = "",
  duration = 2.5,
}: AnimatedCounterProps) {
  const { ref, inView } = useInView({
    triggerOnce: true,
    threshold: 0.3,
  });

  return (
    <span ref={ref}>
      {inView ? (
        <CountUp
          end={end}
          duration={duration}
          prefix={prefix}
          suffix={suffix}
          separator=","
        />
      ) : (
        `${prefix}0${suffix}`
      )}
    </span>
  );
}

export { AnimatedCounter };
