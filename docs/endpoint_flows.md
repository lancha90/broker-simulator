# Diagramas de Flujo - Endpoints API IBKR

## 1. GET /health - Health Check

```mermaid
flowchart TD
    A[Cliente envía GET /health] --> B[HealthController.health_check]
    B --> C[Obtener información del sistema]
    C --> D[psutil.cpu_count, memory, etc.]
    D --> E[platform.system, version, etc.]
    E --> F[Crear HealthResponse]
    F --> G[Retornar status: healthy + server_info]
```

**Características:**
- ✅ Sin autenticación requerida
- ✅ Sin acceso a base de datos
- ✅ Información en tiempo real del servidor

---

## 2. GET /api/v1/balance - Obtener Balance del Usuario

```mermaid
flowchart TD
    A[Cliente envía GET /api/v1/balance<br/>Headers: Authorization: Bearer api_key] --> B[BalanceController.get_balance]
    B --> C[AuthMiddleware.authenticate]
    C --> D[Validar Authorization header]
    D --> E{¿Header válido?}
    E -->|No| F[HTTPException 401<br/>Authorization header missing/invalid]
    E -->|Sí| G[Extraer API key del Bearer token]
    G --> H[UserRepository.find_by_api_key]
    H --> I[Query: SELECT * FROM ibkr_users WHERE api_key = ?]
    I --> J{¿Usuario encontrado?}
    J -->|No| K[HTTPException 401<br/>Invalid API key]
    J -->|Sí| L[Retornar User object]
    L --> M[BalanceService.get_balance]
    M --> N[BalanceRepository.find_by_user_id]
    N --> O[Query: SELECT * FROM ibkr_balances WHERE user_id = ?]
    O --> P{¿Balance existe?}
    P -->|No| Q[BalanceService.create_balance]
    Q --> R[INSERT INTO ibkr_balances]
    R --> S[Retornar nuevo Balance]
    P -->|Sí| T[Retornar Balance existente]
    S --> U[Crear BalanceResponse]
    T --> U
    U --> V[Retornar JSON: user_id, cash_balance]
```

**Características:**
- 🔐 Requiere autenticación con API key
- 💾 Acceso a tablas: `ibkr_users`, `ibkr_balances`
- 🔄 Auto-creación de balance si no existe

---

## 3. GET /api/v1/price/{ticker} - Obtener Precio de Acción

```mermaid
flowchart TD
    A[Cliente envía GET /api/v1/price/AAPL<br/>Headers: Authorization: Bearer api_key] --> B[PriceController.get_price]
    B --> C[AuthMiddleware.authenticate]
    C --> D[Validación de usuario]
    D --> E{¿Usuario válido?}
    E -->|No| F[HTTPException 401]
    E -->|Sí| G[PriceService.get_current_price]
    G --> H[ticker.upper - normalizar símbolo]
    H --> I[Cache.get - verificar caché]
    I --> J{¿Precio en caché?}
    J -->|Sí| K[Retornar precio desde caché]
    J -->|No| L[CompositePriceProvider.get_price]
    L --> M[YahooPriceProvider.get_price]
    M --> N[HTTP GET a Yahoo Finance API]
    N --> O{¿Respuesta exitosa?}
    O -->|No| P[AlphaVantagePriceProvider.get_price]
    P --> Q[HTTP GET a AlphaVantage API]
    Q --> R{¿Respuesta exitosa?}
    R -->|No| S[HTTPException 404<br/>Price not found]
    O -->|Sí| T[Parsear respuesta Yahoo]
    R -->|Sí| U[Parsear respuesta AlphaVantage]
    T --> V[Crear StockPrice object]
    U --> V
    V --> W[Cache.set - guardar en caché por 3 min]
    W --> X[Retornar StockPrice]
    K --> X
    X --> Y[Crear PriceResponse]
    Y --> Z[Retornar JSON: ticker, price, source, timestamp]
```

**Características:**
- 🔐 Requiere autenticación con API key
- 📊 Fuentes de datos: Yahoo Finance (primario), AlphaVantage (respaldo)
- ⚡ Caché en memoria con TTL de 3 minutos
- 🔄 Sistema de fallback entre proveedores

---

## 4. GET /api/v1/portfolio - Obtener Portafolio del Usuario

```mermaid
flowchart TD
    A[Cliente envía GET /api/v1/portfolio<br/>Headers: Authorization: Bearer api_key] --> B[PortfolioController.get_portfolio]
    B --> C[AuthMiddleware.authenticate]
    C --> D[Validación de usuario]
    D --> E{¿Usuario válido?}
    E -->|No| F[HTTPException 401]
    E -->|Sí| G[PortfolioService.get_portfolio]
    G --> H[StockBalanceRepository.find_by_user_id]
    H --> I[Query: SELECT * FROM ibkr_stock_balances WHERE user_id = ?]
    I --> J[Retornar List[StockBalance]]
    J --> K[Mapear a StockHolding objects]
    K --> L[Crear PortfolioResponse]
    L --> M[Retornar JSON: user_id, holdings[]]
```

**Características:**
- 🔐 Requiere autenticación con API key
- 💾 Acceso a tablas: `ibkr_users`, `ibkr_stock_balances`
- 📈 Lista todas las posiciones de acciones del usuario

---

## 5. POST /api/v1/trade - Ejecutar Operación de Trading

```mermaid
flowchart TD
    A[Cliente envía POST /api/v1/trade<br/>Body: ticker, action, quantity, price<br/>Headers: Authorization: Bearer api_key] --> B[TradeController.execute_trade]
    B --> C[AuthMiddleware.authenticate]
    C --> D[Validación de usuario]
    D --> E{¿Usuario válido?}
    E -->|No| F[HTTPException 401]
    E -->|Sí| G[Validar TradeRequest]
    G --> H[Convertir action a TradeType]
    H --> I[TradeService.execute_trade]
    I --> J[Validar datos de entrada]
    J --> K[PriceService.get_current_price]
    K --> L[Obtener precio actual del mercado]
    L --> M{¿Precio válido para trade?}
    M -->|No| N[HTTPException 400<br/>Invalid price for trade type]
    M -->|Sí| O[BalanceService.get_balance]
    O --> P{¿Es operación BUY?}
    P -->|Sí| Q[Validar fondos suficientes]
    Q --> R{¿Fondos suficientes?}
    R -->|No| S[HTTPException 400<br/>Insufficient funds]
    P -->|No| T[StockBalanceRepository.find_by_user_id_and_ticker]
    T --> U{¿Cantidad suficiente para SELL?}
    U -->|No| V[HTTPException 400<br/>Insufficient stock quantity]
    R -->|Sí| W[Crear Trade object]
    U -->|Sí| W
    W --> X[TradeRepository.create]
    X --> Y[INSERT INTO ibkr_trades]
    Y --> Z[Actualizar Balance del usuario]
    Z --> AA{¿Es BUY?}
    AA -->|Sí| BB[Decrementar cash_balance]
    BB --> CC[Actualizar/Crear StockBalance]
    AA -->|No| DD[Incrementar cash_balance]
    DD --> EE[Actualizar StockBalance - reducir quantity]
    CC --> FF[UPDATE ibkr_balances, ibkr_stock_balances]
    EE --> FF
    FF --> GG[Crear TradeResponse]
    GG --> HH[Retornar JSON: id, user_id, ticker, trade_type, quantity, price, total_amount, timestamp]
```

**Características:**
- 🔐 Requiere autenticación con API key
- 💾 Acceso a tablas: `ibkr_users`, `ibkr_balances`, `ibkr_stock_balances`, `ibkr_trades`
- ✅ Validaciones de precios contra mercado
- ✅ Validaciones de fondos y cantidades disponibles
- 🔄 Actualizaciones atómicas de balances y posiciones
- 📊 Soporte para operaciones BUY y SELL

---

## Flujo de Autenticación (Común a todos excepto /health)

```mermaid
flowchart TD
    A[Request con Authorization header] --> B[AuthMiddleware.authenticate]
    B --> C{¿Header Authorization presente?}
    C -->|No| D[HTTPException 401<br/>Authorization header missing]
    C -->|Sí| E{¿Formato Bearer válido?}
    E -->|No| F[HTTPException 401<br/>Invalid authorization header format]
    E -->|Sí| G[Extraer API key]
    G --> H[UserRepository.find_by_api_key]
    H --> I[SELECT * FROM ibkr_users WHERE api_key = ?]
    I --> J{¿Usuario encontrado?}
    J -->|No| K[HTTPException 401<br/>Invalid API key]
    J -->|Sí| L[Retornar User object]
    L --> M[Continuar con endpoint específico]
```

## Arquitectura de Capas

```mermaid
flowchart TD
    A[Web Controllers] --> B[Application Services]
    B --> C[Domain Entities & Repositories]
    C --> D[Infrastructure Adapters]
    D --> E[External Services & Database]
    
    A1[health_controller.py<br/>balance_controller.py<br/>price_controller.py<br/>portfolio_controller.py<br/>trade_controller.py] --> A
    
    B1[BalanceService<br/>PriceService<br/>PortfolioService<br/>TradeService] --> B
    
    C1[User, Balance, StockBalance, Trade<br/>UserRepository, BalanceRepository, etc.] --> C
    
    D1[SupabaseRepositories<br/>YahooPriceProvider<br/>AlphaVantageProvider<br/>MemoryCache] --> D
    
    E1[Supabase DB<br/>Yahoo Finance API<br/>AlphaVantage API] --> E
```

Este diagrama muestra el flujo completo de datos para cada endpoint del sistema IBKR, desde la recepción de la request hasta la respuesta final, incluyendo todas las validaciones, accesos a base de datos y servicios externos involucrados.