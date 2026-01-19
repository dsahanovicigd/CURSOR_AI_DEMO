import { useState } from 'react'

interface FormData {
  // Step 1: Personal Information
  firstName: string
  lastName: string
  dateOfBirth: string
  
  // Step 2: Account Details
  email: string
  username: string
  password: string
  confirmPassword: string
  
  // Step 3: Preferences
  newsletter: boolean
  notifications: boolean
  theme: 'light' | 'dark' | 'auto'
  language: string
  
  // Step 4: Terms
  termsAccepted: boolean
  privacyAccepted: boolean
}

interface FormErrors {
  [key: string]: string
}

const RegistrationForm = () => {
  const [currentStep, setCurrentStep] = useState(1)
  const [formData, setFormData] = useState<FormData>({
    firstName: '',
    lastName: '',
    dateOfBirth: '',
    email: '',
    username: '',
    password: '',
    confirmPassword: '',
    newsletter: false,
    notifications: true,
    theme: 'auto',
    language: 'en',
    termsAccepted: false,
    privacyAccepted: false,
  })
  const [errors, setErrors] = useState<FormErrors>({})
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [touched, setTouched] = useState<{[key: string]: boolean}>({})

  const totalSteps = 4

  // Validation functions
  const validateStep1 = () => {
    const newErrors: FormErrors = {}
    
    if (!formData.firstName.trim()) {
      newErrors.firstName = 'First name is required'
    } else if (formData.firstName.length < 2) {
      newErrors.firstName = 'First name must be at least 2 characters'
    }
    
    if (!formData.lastName.trim()) {
      newErrors.lastName = 'Last name is required'
    } else if (formData.lastName.length < 2) {
      newErrors.lastName = 'Last name must be at least 2 characters'
    }
    
    if (!formData.dateOfBirth) {
      newErrors.dateOfBirth = 'Date of birth is required'
    } else {
      const age = new Date().getFullYear() - new Date(formData.dateOfBirth).getFullYear()
      if (age < 13) {
        newErrors.dateOfBirth = 'You must be at least 13 years old'
      }
    }
    
    return newErrors
  }

  const validateStep2 = () => {
    const newErrors: FormErrors = {}
    
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required'
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address'
    }
    
    if (!formData.username.trim()) {
      newErrors.username = 'Username is required'
    } else if (formData.username.length < 3) {
      newErrors.username = 'Username must be at least 3 characters'
    } else if (!/^[a-zA-Z0-9_]+$/.test(formData.username)) {
      newErrors.username = 'Username can only contain letters, numbers, and underscores'
    }
    
    if (!formData.password) {
      newErrors.password = 'Password is required'
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters'
    } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(formData.password)) {
      newErrors.password = 'Password must contain uppercase, lowercase, and number'
    }
    
    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password'
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match'
    }
    
    return newErrors
  }

  const validateStep3 = () => {
    // Step 3 is optional preferences, no required fields
    return {}
  }

  const validateStep4 = () => {
    const newErrors: FormErrors = {}
    
    if (!formData.termsAccepted) {
      newErrors.termsAccepted = 'You must accept the terms and conditions'
    }
    
    if (!formData.privacyAccepted) {
      newErrors.privacyAccepted = 'You must accept the privacy policy'
    }
    
    return newErrors
  }

  const validateCurrentStep = () => {
    let stepErrors: FormErrors = {}
    
    switch (currentStep) {
      case 1:
        stepErrors = validateStep1()
        break
      case 2:
        stepErrors = validateStep2()
        break
      case 3:
        stepErrors = validateStep3()
        break
      case 4:
        stepErrors = validateStep4()
        break
    }
    
    setErrors(stepErrors)
    return Object.keys(stepErrors).length === 0
  }

  const handleInputChange = (field: keyof FormData, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    
    // Clear error for this field when user starts typing
    if (errors[field]) {
      setErrors(prev => {
        const newErrors = { ...prev }
        delete newErrors[field]
        return newErrors
      })
    }
  }

  const handleBlur = (field: string) => {
    setTouched(prev => ({ ...prev, [field]: true }))
  }

  const handleNext = () => {
    if (validateCurrentStep()) {
      setCurrentStep(prev => Math.min(prev + 1, totalSteps))
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }

  const handleBack = () => {
    setCurrentStep(prev => Math.max(prev - 1, 1))
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const handleStepClick = (step: number) => {
    // Can only go to completed steps or next step
    if (step < currentStep || step === currentStep) {
      setCurrentStep(step)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateCurrentStep()) {
      return
    }
    
    setIsSubmitting(true)
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    setIsSubmitting(false)
    setIsSubmitted(true)
    
    console.log('Form submitted:', formData)
  }

  // Success Screen
  if (isSubmitted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 via-blue-50 to-purple-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full text-center" role="alert" aria-live="polite">
          <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Registration Successful!
          </h1>
          
          <p className="text-gray-600 mb-6">
            Welcome, {formData.firstName}! Your account has been created successfully.
          </p>
          
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6 text-left">
            <h2 className="font-semibold text-blue-900 mb-2">What's next?</h2>
            <ul className="space-y-2 text-sm text-blue-800">
              <li className="flex items-start gap-2">
                <span className="text-blue-600">✓</span>
                <span>Check your email ({formData.email}) for verification</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-600">✓</span>
                <span>Complete your profile to get started</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-600">✓</span>
                <span>Explore our features and documentation</span>
              </li>
            </ul>
          </div>
          
          <button
            onClick={() => window.location.href = '/'}
            className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            aria-label="Go to dashboard"
          >
            Go to Dashboard
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 py-12 px-4">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Create Your Account</h1>
          <p className="text-gray-600">Step {currentStep} of {totalSteps}</p>
        </div>

        {/* Progress Steps */}
        <div className="mb-8" role="navigation" aria-label="Registration progress">
          <div className="flex items-center justify-between relative">
            {/* Progress Line */}
            <div className="absolute top-5 left-0 right-0 h-1 bg-gray-200 -z-10">
              <div 
                className="h-full bg-blue-600 transition-all duration-500"
                style={{ width: `${((currentStep - 1) / (totalSteps - 1)) * 100}%` }}
                role="progressbar"
                aria-valuenow={currentStep}
                aria-valuemin={1}
                aria-valuemax={totalSteps}
                aria-label={`Step ${currentStep} of ${totalSteps}`}
              />
            </div>

            {/* Steps */}
            {[
              { num: 1, label: 'Personal Info' },
              { num: 2, label: 'Account' },
              { num: 3, label: 'Preferences' },
              { num: 4, label: 'Review' },
            ].map(step => (
              <button
                key={step.num}
                onClick={() => handleStepClick(step.num)}
                className={`flex flex-col items-center ${
                  step.num <= currentStep ? 'cursor-pointer' : 'cursor-not-allowed'
                }`}
                disabled={step.num > currentStep}
                aria-label={`${step.label} - Step ${step.num}${step.num === currentStep ? ' (current)' : step.num < currentStep ? ' (completed)' : ''}`}
                aria-current={step.num === currentStep ? 'step' : undefined}
              >
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-all ${
                    step.num < currentStep
                      ? 'bg-green-600 text-white'
                      : step.num === currentStep
                      ? 'bg-blue-600 text-white ring-4 ring-blue-200'
                      : 'bg-gray-200 text-gray-500'
                  }`}
                >
                  {step.num < currentStep ? (
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  ) : (
                    step.num
                  )}
                </div>
                <span className={`mt-2 text-xs sm:text-sm font-medium ${
                  step.num <= currentStep ? 'text-gray-900' : 'text-gray-500'
                }`}>
                  {step.label}
                </span>
              </button>
            ))}
          </div>
        </div>

        {/* Form Card */}
        <div className="bg-white rounded-2xl shadow-xl p-6 sm:p-8">
          <form onSubmit={handleSubmit} noValidate>
            {/* Step 1: Personal Information */}
            {currentStep === 1 && (
              <div role="group" aria-labelledby="step1-heading">
                <h2 id="step1-heading" className="text-2xl font-bold text-gray-900 mb-6">Personal Information</h2>
                
                <div className="space-y-4">
                  {/* First Name */}
                  <div>
                    <label htmlFor="firstName" className="block text-sm font-medium text-gray-700 mb-1">
                      First Name <span className="text-red-500" aria-label="required">*</span>
                    </label>
                    <input
                      type="text"
                      id="firstName"
                      value={formData.firstName}
                      onChange={(e) => handleInputChange('firstName', e.target.value)}
                      onBlur={() => handleBlur('firstName')}
                      className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                        errors.firstName && touched.firstName ? 'border-red-500' : 'border-gray-300'
                      }`}
                      aria-required="true"
                      aria-invalid={errors.firstName && touched.firstName ? 'true' : 'false'}
                      aria-describedby={errors.firstName && touched.firstName ? 'firstName-error' : undefined}
                    />
                    {errors.firstName && touched.firstName && (
                      <p id="firstName-error" className="mt-1 text-sm text-red-600" role="alert">
                        {errors.firstName}
                      </p>
                    )}
                  </div>

                  {/* Last Name */}
                  <div>
                    <label htmlFor="lastName" className="block text-sm font-medium text-gray-700 mb-1">
                      Last Name <span className="text-red-500" aria-label="required">*</span>
                    </label>
                    <input
                      type="text"
                      id="lastName"
                      value={formData.lastName}
                      onChange={(e) => handleInputChange('lastName', e.target.value)}
                      onBlur={() => handleBlur('lastName')}
                      className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                        errors.lastName && touched.lastName ? 'border-red-500' : 'border-gray-300'
                      }`}
                      aria-required="true"
                      aria-invalid={errors.lastName && touched.lastName ? 'true' : 'false'}
                      aria-describedby={errors.lastName && touched.lastName ? 'lastName-error' : undefined}
                    />
                    {errors.lastName && touched.lastName && (
                      <p id="lastName-error" className="mt-1 text-sm text-red-600" role="alert">
                        {errors.lastName}
                      </p>
                    )}
                  </div>

                  {/* Date of Birth */}
                  <div>
                    <label htmlFor="dateOfBirth" className="block text-sm font-medium text-gray-700 mb-1">
                      Date of Birth <span className="text-red-500" aria-label="required">*</span>
                    </label>
                    <input
                      type="date"
                      id="dateOfBirth"
                      value={formData.dateOfBirth}
                      onChange={(e) => handleInputChange('dateOfBirth', e.target.value)}
                      onBlur={() => handleBlur('dateOfBirth')}
                      max={new Date().toISOString().split('T')[0]}
                      className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                        errors.dateOfBirth && touched.dateOfBirth ? 'border-red-500' : 'border-gray-300'
                      }`}
                      aria-required="true"
                      aria-invalid={errors.dateOfBirth && touched.dateOfBirth ? 'true' : 'false'}
                      aria-describedby={errors.dateOfBirth && touched.dateOfBirth ? 'dateOfBirth-error' : undefined}
                    />
                    {errors.dateOfBirth && touched.dateOfBirth && (
                      <p id="dateOfBirth-error" className="mt-1 text-sm text-red-600" role="alert">
                        {errors.dateOfBirth}
                      </p>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* Step 2: Account Details */}
            {currentStep === 2 && (
              <div role="group" aria-labelledby="step2-heading">
                <h2 id="step2-heading" className="text-2xl font-bold text-gray-900 mb-6">Account Details</h2>
                
                <div className="space-y-4">
                  {/* Email */}
                  <div>
                    <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                      Email Address <span className="text-red-500" aria-label="required">*</span>
                    </label>
                    <input
                      type="email"
                      id="email"
                      value={formData.email}
                      onChange={(e) => handleInputChange('email', e.target.value)}
                      onBlur={() => handleBlur('email')}
                      className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                        errors.email && touched.email ? 'border-red-500' : 'border-gray-300'
                      }`}
                      aria-required="true"
                      aria-invalid={errors.email && touched.email ? 'true' : 'false'}
                      aria-describedby={errors.email && touched.email ? 'email-error' : undefined}
                      autoComplete="email"
                    />
                    {errors.email && touched.email && (
                      <p id="email-error" className="mt-1 text-sm text-red-600" role="alert">
                        {errors.email}
                      </p>
                    )}
                  </div>

                  {/* Username */}
                  <div>
                    <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">
                      Username <span className="text-red-500" aria-label="required">*</span>
                    </label>
                    <input
                      type="text"
                      id="username"
                      value={formData.username}
                      onChange={(e) => handleInputChange('username', e.target.value)}
                      onBlur={() => handleBlur('username')}
                      className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                        errors.username && touched.username ? 'border-red-500' : 'border-gray-300'
                      }`}
                      aria-required="true"
                      aria-invalid={errors.username && touched.username ? 'true' : 'false'}
                      aria-describedby={errors.username && touched.username ? 'username-error username-help' : 'username-help'}
                      autoComplete="username"
                    />
                    <p id="username-help" className="mt-1 text-xs text-gray-500">
                      Letters, numbers, and underscores only
                    </p>
                    {errors.username && touched.username && (
                      <p id="username-error" className="mt-1 text-sm text-red-600" role="alert">
                        {errors.username}
                      </p>
                    )}
                  </div>

                  {/* Password */}
                  <div>
                    <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                      Password <span className="text-red-500" aria-label="required">*</span>
                    </label>
                    <input
                      type="password"
                      id="password"
                      value={formData.password}
                      onChange={(e) => handleInputChange('password', e.target.value)}
                      onBlur={() => handleBlur('password')}
                      className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                        errors.password && touched.password ? 'border-red-500' : 'border-gray-300'
                      }`}
                      aria-required="true"
                      aria-invalid={errors.password && touched.password ? 'true' : 'false'}
                      aria-describedby={errors.password && touched.password ? 'password-error password-help' : 'password-help'}
                      autoComplete="new-password"
                    />
                    <p id="password-help" className="mt-1 text-xs text-gray-500">
                      At least 8 characters with uppercase, lowercase, and number
                    </p>
                    {errors.password && touched.password && (
                      <p id="password-error" className="mt-1 text-sm text-red-600" role="alert">
                        {errors.password}
                      </p>
                    )}
                  </div>

                  {/* Confirm Password */}
                  <div>
                    <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
                      Confirm Password <span className="text-red-500" aria-label="required">*</span>
                    </label>
                    <input
                      type="password"
                      id="confirmPassword"
                      value={formData.confirmPassword}
                      onChange={(e) => handleInputChange('confirmPassword', e.target.value)}
                      onBlur={() => handleBlur('confirmPassword')}
                      className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                        errors.confirmPassword && touched.confirmPassword ? 'border-red-500' : 'border-gray-300'
                      }`}
                      aria-required="true"
                      aria-invalid={errors.confirmPassword && touched.confirmPassword ? 'true' : 'false'}
                      aria-describedby={errors.confirmPassword && touched.confirmPassword ? 'confirmPassword-error' : undefined}
                      autoComplete="new-password"
                    />
                    {errors.confirmPassword && touched.confirmPassword && (
                      <p id="confirmPassword-error" className="mt-1 text-sm text-red-600" role="alert">
                        {errors.confirmPassword}
                      </p>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* Step 3: Preferences */}
            {currentStep === 3 && (
              <div role="group" aria-labelledby="step3-heading">
                <h2 id="step3-heading" className="text-2xl font-bold text-gray-900 mb-2">Preferences</h2>
                <p className="text-gray-600 mb-6">Customize your experience (optional)</p>
                
                <div className="space-y-6">
                  {/* Notification Preferences */}
                  <div>
                    <h3 className="text-sm font-semibold text-gray-900 mb-3">Notifications</h3>
                    <div className="space-y-3">
                      <div className="flex items-center">
                        <input
                          type="checkbox"
                          id="newsletter"
                          checked={formData.newsletter}
                          onChange={(e) => handleInputChange('newsletter', e.target.checked)}
                          className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                        />
                        <label htmlFor="newsletter" className="ml-3 text-sm text-gray-700">
                          Subscribe to newsletter for updates and tips
                        </label>
                      </div>
                      
                      <div className="flex items-center">
                        <input
                          type="checkbox"
                          id="notifications"
                          checked={formData.notifications}
                          onChange={(e) => handleInputChange('notifications', e.target.checked)}
                          className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                        />
                        <label htmlFor="notifications" className="ml-3 text-sm text-gray-700">
                          Enable push notifications
                        </label>
                      </div>
                    </div>
                  </div>

                  {/* Theme */}
                  <div>
                    <label htmlFor="theme" className="block text-sm font-semibold text-gray-900 mb-3">
                      Theme Preference
                    </label>
                    <select
                      id="theme"
                      value={formData.theme}
                      onChange={(e) => handleInputChange('theme', e.target.value as 'light' | 'dark' | 'auto')}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="auto">Auto (System Preference)</option>
                      <option value="light">Light Mode</option>
                      <option value="dark">Dark Mode</option>
                    </select>
                  </div>

                  {/* Language */}
                  <div>
                    <label htmlFor="language" className="block text-sm font-semibold text-gray-900 mb-3">
                      Language
                    </label>
                    <select
                      id="language"
                      value={formData.language}
                      onChange={(e) => handleInputChange('language', e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="en">English</option>
                      <option value="es">Español</option>
                      <option value="fr">Français</option>
                      <option value="de">Deutsch</option>
                      <option value="ja">日本語</option>
                    </select>
                  </div>
                </div>
              </div>
            )}

            {/* Step 4: Review & Terms */}
            {currentStep === 4 && (
              <div role="group" aria-labelledby="step4-heading">
                <h2 id="step4-heading" className="text-2xl font-bold text-gray-900 mb-6">Review & Accept</h2>
                
                {/* Summary */}
                <div className="bg-gray-50 rounded-lg p-6 mb-6">
                  <h3 className="text-sm font-semibold text-gray-900 mb-4">Registration Summary</h3>
                  <dl className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <dt className="text-gray-600">Name:</dt>
                      <dd className="font-medium text-gray-900">{formData.firstName} {formData.lastName}</dd>
                    </div>
                    <div className="flex justify-between">
                      <dt className="text-gray-600">Email:</dt>
                      <dd className="font-medium text-gray-900">{formData.email}</dd>
                    </div>
                    <div className="flex justify-between">
                      <dt className="text-gray-600">Username:</dt>
                      <dd className="font-medium text-gray-900">@{formData.username}</dd>
                    </div>
                    <div className="flex justify-between">
                      <dt className="text-gray-600">Date of Birth:</dt>
                      <dd className="font-medium text-gray-900">{formData.dateOfBirth}</dd>
                    </div>
                    <div className="flex justify-between">
                      <dt className="text-gray-600">Newsletter:</dt>
                      <dd className="font-medium text-gray-900">{formData.newsletter ? 'Yes' : 'No'}</dd>
                    </div>
                    <div className="flex justify-between">
                      <dt className="text-gray-600">Theme:</dt>
                      <dd className="font-medium text-gray-900 capitalize">{formData.theme}</dd>
                    </div>
                  </dl>
                </div>

                {/* Terms */}
                <div className="space-y-4">
                  <div className="flex items-start">
                    <input
                      type="checkbox"
                      id="termsAccepted"
                      checked={formData.termsAccepted}
                      onChange={(e) => handleInputChange('termsAccepted', e.target.checked)}
                      className={`mt-1 w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500 ${
                        errors.termsAccepted ? 'border-red-500' : ''
                      }`}
                      aria-required="true"
                      aria-invalid={errors.termsAccepted ? 'true' : 'false'}
                      aria-describedby={errors.termsAccepted ? 'terms-error' : undefined}
                    />
                    <label htmlFor="termsAccepted" className="ml-3 text-sm text-gray-700">
                      I accept the <a href="#" className="text-blue-600 hover:underline">Terms and Conditions</a>
                      <span className="text-red-500" aria-label="required"> *</span>
                    </label>
                  </div>
                  {errors.termsAccepted && (
                    <p id="terms-error" className="text-sm text-red-600 ml-7" role="alert">
                      {errors.termsAccepted}
                    </p>
                  )}

                  <div className="flex items-start">
                    <input
                      type="checkbox"
                      id="privacyAccepted"
                      checked={formData.privacyAccepted}
                      onChange={(e) => handleInputChange('privacyAccepted', e.target.checked)}
                      className={`mt-1 w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500 ${
                        errors.privacyAccepted ? 'border-red-500' : ''
                      }`}
                      aria-required="true"
                      aria-invalid={errors.privacyAccepted ? 'true' : 'false'}
                      aria-describedby={errors.privacyAccepted ? 'privacy-error' : undefined}
                    />
                    <label htmlFor="privacyAccepted" className="ml-3 text-sm text-gray-700">
                      I accept the <a href="#" className="text-blue-600 hover:underline">Privacy Policy</a>
                      <span className="text-red-500" aria-label="required"> *</span>
                    </label>
                  </div>
                  {errors.privacyAccepted && (
                    <p id="privacy-error" className="text-sm text-red-600 ml-7" role="alert">
                      {errors.privacyAccepted}
                    </p>
                  )}
                </div>
              </div>
            )}

            {/* Navigation Buttons */}
            <div className="flex gap-4 mt-8">
              {currentStep > 1 && (
                <button
                  type="button"
                  onClick={handleBack}
                  className="flex-1 px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition-colors"
                  aria-label="Go to previous step"
                >
                  Back
                </button>
              )}
              
              {currentStep < totalSteps ? (
                <button
                  type="button"
                  onClick={handleNext}
                  className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors"
                  aria-label="Go to next step"
                >
                  Next
                </button>
              ) : (
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className={`flex-1 px-6 py-3 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 transition-colors flex items-center justify-center gap-2 ${
                    isSubmitting ? 'opacity-75 cursor-not-allowed' : ''
                  }`}
                  aria-label="Submit registration form"
                  aria-busy={isSubmitting}
                >
                  {isSubmitting ? (
                    <>
                      <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24" aria-hidden="true">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                      <span>Submitting...</span>
                    </>
                  ) : (
                    'Complete Registration'
                  )}
                </button>
              )}
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default RegistrationForm
