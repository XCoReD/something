# Radio Backend Service

A comprehensive backend service with admin frontend for managing audio data units and their storage.

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application and routes
│   │   ├── models.py            # SQLAlchemy database models
│   │   ├── schemas.py           # Pydantic models for validation
│   │   ├── database.py          # Database connection setup
│   │   ├── crud.py             # Database operations
│   │   ├── auth.py             # Authentication logic
│   │   └── utils/
│   │       └── audio.py        # Audio processing utilities
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.tsx             # Main application component
│   │   ├── types.ts            # TypeScript type definitions
│   │   ├── api/
│   │   │   └── index.ts        # API integration layer
│   │   ├── components/
│   │   │   └── AudioPlayer.tsx # Audio playback component
│   │   └── store/
│   │       └── auth.ts         # Authentication state management
│   └── package.json            # Node.js dependencies
└── README.md                   # This documentation
```

## Features

### Backend Services

1. Data Unit Storage Management
   - Create, enable/disable, and remove storage units
   - Configure metadata fields:
     - Voice type selection
     - Translation start time
     - Translation interruption settings

2. Data Unit Management
   - List, enable/disable individual units
   - Reorder units within storage
   - Transactional editing with apply/revert functionality

3. Content Management
   - Support for up to 3 description-audio pairs per unit
   - Audio track management:
     - Upload support
     - Auto-generation from description
     - Automatic normalization (128Kbps CBR, 44.1KHz, 2 channels)

4. Authentication & Authorization
   - JWT-based authentication
   - Role-based access control:
     - Viewer: Read-only access
     - Editor: Modification rights
     - Supervisor: Editor rights + service management

### Frontend Features

1. User Interface
   - Role-based access control
   - Audio file management:
     - Upload support (mp3, wav, ogg, avi)
     - Maximum file size: 200MB
     - In-browser playback
     - Download functionality

2. Data Management
   - Single-page editing for all units in storage
   - Pagination options (10, 20, 50, 100, all)
   - Local state persistence for unsaved changes
   - Transaction-based changes with apply/revert

3. Internationalization
   - Centralized UX terms storage
   - Easy translation support

## Technical Requirements

### Backend

- Python 3.8+
- FastAPI
- SQLAlchemy
- pydub for audio processing
- Additional dependencies in requirements.txt

### Frontend

- Node.js 16+
- TypeScript
- React 18
- Tailwind CSS
- Additional dependencies in package.json

## Getting Started

1. Backend Setup
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

2. Frontend Setup
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## API Endpoints

### Authentication
- POST /auth/token - Get access token
- GET /auth/me - Get current user info

### Storage Management
- GET /storage/ - List all storages
- POST /storage/ - Create new storage
- PUT /storage/{storage_id}/status - Update storage status
- DELETE /storage/{storage_id} - Remove storage

### Data Unit Management
- GET /storage/{storage_id}/units - List units in storage
- POST /storage/{storage_id}/unit/ - Create new unit
- PUT /storage/{storage_id}/units/reorder - Reorder units
- PUT /storage/{storage_id}/unit/{unit_id}/status - Update unit status

### Audio Management
- POST /storage/unit/{unit_id}/audio - Upload audio file
- GET /storage/unit/{unit_id}/audio/{audio_id} - Download audio file
- PUT /storage/unit/{unit_id}/audio/generate - Generate audio from description

### System Management
- POST /service/restart - Restart services (Supervisor only)

## Security

1. Authentication
   - JWT-based token authentication
   - Secure password hashing with bcrypt

2. Authorization
   - Role-based access control
   - Endpoint-level permission checking

3. File Security
   - File type validation
   - Size limitations
   - Secure file storage

## Error Handling

1. Backend
   - HTTP status codes
   - Detailed error messages
   - Transaction rollback on failures

2. Frontend
   - User-friendly error messages
   - Form validation
   - Network error handling

## Future Enhancements

1. Audio Processing
   - Additional audio format support
   - Advanced audio normalization options
   - Real text-to-speech integration

2. User Management
   - User registration
   - Password reset
   - Session management

3. Monitoring
   - System health metrics
   - Usage statistics
   - Audit logging

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.