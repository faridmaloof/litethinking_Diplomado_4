export type HttpMethod = 'GET' | 'POST'

export interface MockScenario {
  id: string
  label: string
  description: string
  method: HttpMethod
  path: string
  requestBody?: Record<string, unknown>
  expectedStatus: number
  expectedBody: Record<string, unknown>
}

export const mockScenarios: MockScenario[] = [
  {
    id: 'health-200',
    label: 'Health check',
    description: 'Valida disponibilidad del mock de salud.',
    method: 'GET',
    path: '/api/health',
    expectedStatus: 200,
    expectedBody: {
      status: 'UP',
      servicio: 'wiremock-dia2',
    },
  },
  {
    id: 'pagos-aprobado-201',
    label: 'Pago aprobado',
    description: 'Valida la respuesta de aprobacion del endpoint de pagos.',
    method: 'POST',
    path: '/api/pagos/aprobado',
    requestBody: {
      monto: 150.25,
      moneda: 'CLP',
      comercio: 'Tienda QA',
    },
    expectedStatus: 201,
    expectedBody: {
      id_transaccion: 'TX-1001',
      estado: 'APROBADO',
      codigo: 'OK_205',
    },
  },
  {
    id: 'pagos-timeout-504',
    label: 'Pago timeout',
    description: 'Valida el mock de timeout de banco con estado 504.',
    method: 'POST',
    path: '/api/pagos',
    requestBody: {
      monto: 999.99,
      moneda: 'CLP',
      comercio: 'Banco simulacion',
    },
    expectedStatus: 504,
    expectedBody: {
      error: 'Gateway Timeout - Banco Caído',
      codigo: 'ERR_504',
    },
  },
]