import type { LabState } from '../types/lab'

interface AccessibilitySectionProps {
  data: LabState | null
}

export function AccessibilitySection({ data }: AccessibilitySectionProps) {
  return (
    <article className="card">
      <div className="section-header">
        <div>
          <p className="eyebrow">Accesibilidad</p>
          <h2>DOM legible, etiquetas y foco visible</h2>
        </div>
      </div>

      <form className="demo-form" aria-label="Formulario accesible de prueba" onSubmit={(event) => event.preventDefault()}>
        <label>
          Nombre completo
          <input type="text" placeholder="Ana Perez" />
        </label>
        <label>
          Correo electronico
          <input type="email" placeholder="ana@dominio.com" />
        </label>
        <label>
          Mensaje de localizacion
          <textarea rows={3} placeholder={data?.content.localeLabel ?? 'Texto largo'} />
        </label>
        <button type="submit">Enviar muestra</button>
      </form>

      <div className="list-box">
        <h3>Se puede validar con teclado</h3>
        <ul>
          {data?.accessibility.testing?.map((item) => <li key={item}>{item}</li>)}
        </ul>
      </div>

      <div className="list-box accent">
        <h3>Señales incluidas</h3>
        <ul>
          {data?.accessibility.signals?.map((item) => <li key={item}>{item}</li>)}
        </ul>
      </div>
    </article>
  )
}
