interface BarProps {
  value: number
  max: number
}

export function Bar({ value, max }: BarProps) {
  const percent = Math.min(100, Math.max(0, (value / max) * 100))

  return (
    <div className="bar-track" aria-hidden="true">
      <div className="bar-fill" style={{ width: `${percent}%` }} />
    </div>
  )
}
