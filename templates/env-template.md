# Environment Variables — {project-name}
#
# Copy this file to .env and fill in your values.
# Never commit .env to version control.
# Updated: YYYY-MM-DD
#
# Legend:
#   # REQUIRED  — app will fail to start without this
#   # OPTIONAL  — has a sensible default or feature is disabled

# =============================================================================
# APPLICATION
# =============================================================================

APP_ENV=development              # REQUIRED  — development | staging | production
APP_PORT=3000                    # OPTIONAL  — default: 3000
APP_SECRET_KEY=changeme          # REQUIRED  — secret for sessions/JWT signing
APP_DEBUG=true                   # OPTIONAL  — enable debug logging

# =============================================================================
# DATABASE
# =============================================================================

DATABASE_URL=postgresql://user:password@localhost:5432/dbname  # REQUIRED
# DATABASE_POOL_SIZE=10          # OPTIONAL

# =============================================================================
# AUTHENTICATION
# =============================================================================

AUTH_JWT_SECRET=changeme         # REQUIRED
AUTH_JWT_EXPIRES_IN=7d           # OPTIONAL  — default: 7d
# AUTH_GOOGLE_CLIENT_ID=         # OPTIONAL  — enable Google OAuth
# AUTH_GOOGLE_CLIENT_SECRET=     # OPTIONAL

# =============================================================================
# EXTERNAL APIS
# =============================================================================

# {SERVICE_NAME}_API_KEY=        # REQUIRED (if using {service})
# {SERVICE_NAME}_API_URL=        # REQUIRED (if using {service})

# =============================================================================
# STORAGE
# =============================================================================

# STORAGE_PROVIDER=s3            # OPTIONAL  — local | s3 | gcs
# AWS_ACCESS_KEY_ID=             # REQUIRED if STORAGE_PROVIDER=s3
# AWS_SECRET_ACCESS_KEY=         # REQUIRED if STORAGE_PROVIDER=s3
# AWS_S3_BUCKET=                 # REQUIRED if STORAGE_PROVIDER=s3
# AWS_REGION=us-east-1           # OPTIONAL  — default: us-east-1

# =============================================================================
# EMAIL
# =============================================================================

# SMTP_HOST=smtp.example.com     # REQUIRED (if sending email)
# SMTP_PORT=587                  # OPTIONAL  — default: 587
# SMTP_USER=                     # REQUIRED (if sending email)
# SMTP_PASS=                     # REQUIRED (if sending email)
# EMAIL_FROM=noreply@example.com # OPTIONAL

# =============================================================================
# FEATURE FLAGS
# =============================================================================

# FEATURE_{NAME}_ENABLED=false   # OPTIONAL  — toggle features without deploy

# =============================================================================
# MONITORING & OBSERVABILITY
# =============================================================================

# SENTRY_DSN=                    # OPTIONAL  — enable error tracking
# LOG_LEVEL=info                 # OPTIONAL  — debug | info | warn | error
