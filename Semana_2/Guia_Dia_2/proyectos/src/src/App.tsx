import { useEffect, useMemo, useState } from 'react'
import './App.css'
import { callApi } from './lib/apiClient'
import { mockScenarios } from './lib/scenarios'
import type { MockScenario } from './lib/scenarios'
import { validateScenario } from './lib/validator'

interface Product {
  id: string
  name: string
  description: string
  price: number
}

interface PaymentForm {
  customerName: string
  email: string
  cardLast4: string
  scenarioId: 'pagos-aprobado-201' | 'pagos-timeout-504'
}

interface PaymentResult {
  approved: boolean
  title: string
  message: string
  elapsedMs: number
  status: number
  body: unknown
  issues: { field: string; message: string; expected: unknown; actual: unknown }[]
}

type ViewStep = 'store' | 'checkout' | 'result'

const products: Product[] = [
  {
    id: 'headphones',
    name: 'Auriculares Wave Pro',
    description: 'Audio inalambrico con cancelacion de ruido.',
    price: 12990,
  },
  {
    id: 'speaker',
    name: 'Parlante Move Mini',
    description: 'Bluetooth, 10 horas de bateria y resistencia al agua.',
    price: 18990,
  },
]

function formatCurrency(value: number): string {
  return new Intl.NumberFormat('es-CL', {
    style: 'currency',
    currency: 'CLP',
    maximumFractionDigits: 0,
  }).format(value)
}

function prettyJson(value: unknown): string {
  try {
    return JSON.stringify(value, null, 2)
  } catch {
    return String(value)
  }
}

function findScenario(id: PaymentForm['scenarioId']): MockScenario {
  const scenario = mockScenarios.find((item) => item.id === id)
  if (!scenario) {
    throw new Error(`Scenario ${id} was not found`)
  }
  return scenario
}

function App() {
  const cartItems = useMemo(() => products, [])
  const total = useMemo(
    () => cartItems.reduce((accumulator, item) => accumulator + item.price, 0),
    [cartItems],
  )

  const [healthText, setHealthText] = useState('Verificando servicio de pagos...')
  const [view, setView] = useState<ViewStep>('store')
  const [isProcessing, setIsProcessing] = useState(false)
  const [showTechDetails, setShowTechDetails] = useState(false)
  const [form, setForm] = useState<PaymentForm>({
    customerName: '',
    email: '',
    cardLast4: '',
    scenarioId: 'pagos-aprobado-201',
  })
  const [result, setResult] = useState<PaymentResult | null>(null)

  useEffect(() => {
    let isMounted = true

    async function checkHealth(): Promise<void> {
      try {
        const healthScenario = mockScenarios.find((item) => item.id === 'health-200')
        if (!healthScenario) {
          return
        }

        const response = await callApi(healthScenario.method, healthScenario.path)
        const validation = validateScenario(
          healthScenario.expectedStatus,
          healthScenario.expectedBody,
          response.status,
          response.body,
        )

        if (!isMounted) {
          return
        }

        setHealthText(
          validation.pass
            ? 'Servicio de pagos disponible'
            : 'Servicio disponible con respuesta inesperada',
        )
      } catch {
        if (isMounted) {
          setHealthText('Servicio de pagos no disponible en este momento')
        }
      }
    }

    void checkHealth()

    return () => {
      isMounted = false
    }
  }, [])

  const handleInputChange = (field: keyof PaymentForm, value: string) => {
    setForm((current) => ({ ...current, [field]: value }))
  }

  const goToCheckout = () => {
    setView('checkout')
    setShowTechDetails(false)
  }

  const goToStore = () => {
    setView('store')
  }

  const placeOrder = async () => {
    if (!form.customerName || !form.email || form.cardLast4.length !== 4) {
      return
    }

    setIsProcessing(true)
    setShowTechDetails(false)

    try {
      const scenario = findScenario(form.scenarioId)
      const response = await callApi(scenario.method, scenario.path, {
        ...scenario.requestBody,
        cliente: form.customerName,
        email: form.email,
        total,
      })
      const validation = validateScenario(
        scenario.expectedStatus,
        scenario.expectedBody,
        response.status,
        response.body,
      )

      const approved = validation.pass && scenario.id === 'pagos-aprobado-201'

      setResult({
        approved,
        title: approved ? 'Pago aprobado' : 'Pago no aprobado',
        message: approved
          ? 'Tu compra fue procesada correctamente. Enviaremos el comprobante a tu correo.'
          : 'No pudimos confirmar el pago. Intenta nuevamente en unos minutos.',
        elapsedMs: response.elapsedMs,
        status: response.status,
        body: response.body,
        issues: validation.issues,
      })
    } catch {
      setResult({
        approved: false,
        title: 'Pago no aprobado',
        message: 'Ocurrio un error de comunicacion con el servicio de pagos.',
        elapsedMs: 0,
        status: 0,
        body: null,
        issues: [
          {
            field: 'network',
            message: 'No se pudo completar la solicitud de pago.',
            expected: 'Respuesta valida del servicio',
            actual: 'Error de conexion',
          },
        ],
      })
    } finally {
      setIsProcessing(false)
      setView('result')
    }
  }

  const canSubmit =
    form.customerName.trim().length > 2 &&
    form.email.includes('@') &&
    /^[0-9]{4}$/.test(form.cardLast4)

  return (
    <main className="shop-page">
      <header className="topbar">
        <div>
          <p className="brand">NovaShop</p>
          <h1>Checkout de pago</h1>
        </div>
        <p className="health-pill">{healthText}</p>
      </header>

      {view === 'store' && (
        <section className="panel">
          <h2>Tu carrito</h2>
          <p className="muted">Revisa tus productos antes de continuar al pago.</p>

          <ul className="cart-list">
            {cartItems.map((item) => (
              <li key={item.id}>
                <div>
                  <h3>{item.name}</h3>
                  <p>{item.description}</p>
                </div>
                <strong>{formatCurrency(item.price)}</strong>
              </li>
            ))}
          </ul>

          <div className="summary">
            <span>Total</span>
            <strong>{formatCurrency(total)}</strong>
          </div>

          <button type="button" className="primary-button" onClick={goToCheckout}>
            Continuar al pago
          </button>
        </section>
      )}

      {view === 'checkout' && (
        <section className="panel">
          <h2>Datos de pago</h2>
          <p className="muted">Completa la informacion para procesar tu orden.</p>

          <form
            className="checkout-form"
            onSubmit={(event) => {
              event.preventDefault()
              void placeOrder()
            }}
          >
            <label>
              Nombre completo
              <input
                value={form.customerName}
                onChange={(event) => handleInputChange('customerName', event.target.value)}
                placeholder="Ejemplo: Ana Perez"
              />
            </label>

            <label>
              Correo electronico
              <input
                type="email"
                value={form.email}
                onChange={(event) => handleInputChange('email', event.target.value)}
                placeholder="correo@dominio.com"
              />
            </label>

            <label>
              Ultimos 4 digitos de tarjeta
              <input
                value={form.cardLast4}
                onChange={(event) =>
                  handleInputChange('cardLast4', event.target.value.replace(/\D/g, '').slice(0, 4))
                }
                placeholder="1234"
              />
            </label>

            <label>
              Canal bancario para simulacion
              <select
                value={form.scenarioId}
                onChange={(event) =>
                  handleInputChange(
                    'scenarioId',
                    event.target.value as PaymentForm['scenarioId'],
                  )
                }
              >
                <option value="pagos-aprobado-201">Banco principal (aprobacion esperada)</option>
                <option value="pagos-timeout-504">Banco contingencia (rechazo por timeout)</option>
              </select>
            </label>

            <div className="summary compact">
              <span>Total a pagar</span>
              <strong>{formatCurrency(total)}</strong>
            </div>

            <div className="actions">
              <button type="button" className="ghost-button" onClick={goToStore}>
                Volver
              </button>
              <button
                type="submit"
                className="primary-button"
                disabled={!canSubmit || isProcessing}
              >
                {isProcessing ? 'Procesando pago...' : 'Pagar ahora'}
              </button>
            </div>
          </form>
        </section>
      )}

      {view === 'result' && result && (
        <section className="panel">
          <h2 className={result.approved ? 'approved' : 'rejected'}>{result.title}</h2>
          <p className="muted">{result.message}</p>

          <div className="result-highlight">
            <span>Estado de transaccion</span>
            <strong>{result.approved ? 'APROBADO' : 'NO APROBADO'}</strong>
          </div>

          <div className="result-meta">
            <p>Codigo HTTP: {result.status || 'Sin respuesta'}</p>
            <p>Tiempo de respuesta: {result.elapsedMs} ms</p>
          </div>

          <button
            type="button"
            className="ghost-button"
            onClick={() => setShowTechDetails((current) => !current)}
          >
            {showTechDetails ? 'Ocultar detalle tecnico' : 'Ver detalle tecnico'}
          </button>

          {showTechDetails && (
            <div className="technical-box">
              <h3>Respuesta del servicio</h3>
              <pre>{prettyJson(result.body)}</pre>
              {result.issues.length > 0 && (
                <>
                  <h3>Diferencias detectadas</h3>
                  <ul>
                    {result.issues.map((issue) => (
                      <li key={`${issue.field}-${issue.message}`}>
                        <strong>{issue.field}</strong>: {issue.message}
                      </li>
                    ))}
                  </ul>
                </>
              )}
            </div>
          )}

          <div className="actions">
            <button
              type="button"
              className="ghost-button"
              onClick={() => {
                setView('checkout')
                setShowTechDetails(false)
              }}
            >
              Reintentar pago
            </button>
            <button
              type="button"
              className="primary-button"
              onClick={() => {
                setView('store')
                setShowTechDetails(false)
              }}
            >
              Volver a la tienda
            </button>
          </div>
        </section>
      )}
    </main>
  )
}

export default App
