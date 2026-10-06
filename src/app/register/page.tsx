import { signUp } from '@/actions/auth'
import ProfileFields from '@/components/ProfileFields'

export default function RegisterPage({
  searchParams,
}: {
  searchParams: { error?: string }
}) {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-lg bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900">Create your account</h1>
          <p className="text-sm text-gray-500 mt-1">Biomanufacturing Facility Map</p>
        </div>

        {searchParams.error && (
          <div className="mb-6 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
            {decodeURIComponent(searchParams.error)}
          </div>
        )}

        <form action={signUp} className="space-y-6">
          {/* Account credentials */}
          <div>
            <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Account</p>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email address <span className="text-red-500">*</span>
              </label>
              <input
                name="email"
                type="email"
                required
                autoComplete="email"
                className="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>
            <div className="grid grid-cols-2 gap-3 mt-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Password <span className="text-red-500">*</span>
                </label>
                <input
                  name="password"
                  type="password"
                  required
                  minLength={6}
                  autoComplete="new-password"
                  className="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Confirm password <span className="text-red-500">*</span>
                </label>
                <input
                  name="confirmPassword"
                  type="password"
                  required
                  minLength={6}
                  autoComplete="new-password"
                  className="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                />
              </div>
            </div>
          </div>

          <div className="border-t border-gray-100" />

          {/* Profile fields */}
          <ProfileFields />

          <div className="border-t border-gray-100" />

          {/* Privacy policy */}
          <div className="flex items-start gap-3">
            <input
              id="privacy"
              name="privacy"
              type="checkbox"
              required
              className="mt-0.5 h-4 w-4 rounded border-gray-300 text-emerald-600 focus:ring-emerald-500"
            />
            <label htmlFor="privacy" className="text-sm text-gray-600">
              I agree to the{' '}
              <a href="/privacy" className="text-emerald-700 hover:underline">Privacy &amp; Cookie Policy</a>
              {' '}<span className="text-red-500">*</span>
            </label>
          </div>

          <button
            type="submit"
            className="w-full py-2.5 px-4 bg-emerald-600 text-white text-sm font-semibold rounded-lg hover:bg-emerald-700 transition-colors"
          >
            Create account
          </button>
        </form>

        <p className="mt-6 text-sm text-center text-gray-500">
          Already have an account?{' '}
          <a href="/login" className="text-emerald-700 hover:underline font-medium">Sign in</a>
        </p>
      </div>
    </div>
  )
}
