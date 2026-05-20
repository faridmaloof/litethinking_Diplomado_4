export interface ValidationIssue {
  field: string
  expected: unknown
  actual: unknown
  message: string
}

export interface ValidationResult {
  pass: boolean
  issues: ValidationIssue[]
}

function isPlainObject(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

function compareExact(
  expected: unknown,
  actual: unknown,
  currentPath: string,
  issues: ValidationIssue[],
): void {
  if (Array.isArray(expected) && Array.isArray(actual)) {
    if (expected.length !== actual.length) {
      issues.push({
        field: currentPath,
        expected: expected.length,
        actual: actual.length,
        message: 'Array length does not match.',
      })
      return
    }

    for (let index = 0; index < expected.length; index += 1) {
      compareExact(expected[index], actual[index], `${currentPath}[${index}]`, issues)
    }
    return
  }

  if (isPlainObject(expected) && isPlainObject(actual)) {
    const expectedKeys = Object.keys(expected)
    const actualKeys = Object.keys(actual)

    for (const key of expectedKeys) {
      if (!(key in actual)) {
        issues.push({
          field: `${currentPath}.${key}`,
          expected: expected[key],
          actual: undefined,
          message: 'Expected field is missing.',
        })
        continue
      }

      compareExact(expected[key], actual[key], `${currentPath}.${key}`, issues)
    }

    for (const key of actualKeys) {
      if (!(key in expected)) {
        issues.push({
          field: `${currentPath}.${key}`,
          expected: undefined,
          actual: actual[key],
          message: 'Unexpected extra field present.',
        })
      }
    }
    return
  }

  if (expected !== actual) {
    issues.push({
      field: currentPath,
      expected,
      actual,
      message: 'Value does not match.',
    })
  }
}

export function validateScenario(
  expectedStatus: number,
  expectedBody: unknown,
  receivedStatus: number,
  receivedBody: unknown,
): ValidationResult {
  const issues: ValidationIssue[] = []

  if (expectedStatus !== receivedStatus) {
    issues.push({
      field: 'status',
      expected: expectedStatus,
      actual: receivedStatus,
      message: 'Status code does not match.',
    })
  }

  compareExact(expectedBody, receivedBody, 'body', issues)

  return {
    pass: issues.length === 0,
    issues,
  }
}