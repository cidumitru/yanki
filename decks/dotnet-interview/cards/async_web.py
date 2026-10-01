"""Async/threading (11 cards) and ASP.NET Core (17 cards)."""

ASYNC = ["dotnet::async"]
WEB = ["dotnet::aspnetcore"]

CARDS = [
    # ---------------------------------------------------------------- async
    dict(
        id="A01", tags=ASYNC,
        q="What does `async`/`await` actually do?",
        a="`async` marks a method so the compiler rewrites it into a state machine. `await` on an incomplete awaitable registers the rest of the method as a continuation, returns an incomplete `Task` to the caller, and frees the current thread. When the awaited operation completes, the continuation resumes (on the captured context, if any). It is about not blocking threads during I/O, not about running code on more threads.",
        why="The core async question; the common misconception is that `await` starts a new thread.",
        ex="""```
public async Task<string> LoadAsync(HttpClient http)
{
    var json = await http.GetStringAsync("/api");   // thread released while waiting
    return json.ToUpperInvariant();                 // continuation
}
```""",
        src="https://learn.microsoft.com/dotnet/csharp/asynchronous-programming/",
    ),
    dict(
        id="A02", tags=ASYNC,
        q="What is the difference between a `Task` and a `Thread`?",
        a="A `Thread` is an OS-level execution unit you create and manage yourself — expensive (about 1 MB of stack) and not composable. A `Task` is a promise of a result from some operation: CPU-bound tasks are scheduled onto the thread pool, while I/O-bound tasks complete through OS callbacks and may occupy no thread at all. Tasks support continuations, cancellation, exception propagation and `await`.",
        why="Clarifies that async I/O does not consume threads and why raw threads are rarely the right tool.",
        ex="`await File.ReadAllTextAsync(path)` uses no thread while the disk works; `new Thread(() => Crunch()).Start()` dedicates an OS thread to CPU work.",
        src="https://learn.microsoft.com/dotnet/standard/parallel-programming/task-based-asynchronous-programming",
    ),
    dict(
        id="A03", tags=ASYNC,
        q="When should you use `Task.Run`, and why is it discouraged inside ASP.NET Core request handling?",
        a="Use `Task.Run` to push CPU-bound work off a UI thread, or to parallelize CPU work in a desktop or console app. In ASP.NET Core each request already runs on a thread-pool thread, so `Task.Run` just moves the work to another pool thread, adding overhead and risking thread-pool starvation under load. For I/O use genuinely async APIs; never wrap synchronous I/O in `Task.Run` to \"make it async\".",
        why="Distinguishes I/O-bound from CPU-bound async — a key senior-level distinction.",
        ex="""```
// Good (WPF):          var primes = await Task.Run(() => ComputePrimes(1_000_000));
// Bad (ASP.NET Core):  var text = await Task.Run(() => File.ReadAllText(path));
// Right:               var text = await File.ReadAllTextAsync(path, ct);
```""",
        src="https://learn.microsoft.com/aspnet/core/fundamentals/best-practices",
    ),
    dict(
        id="A04", tags=ASYNC,
        q="Why should you avoid `async void` methods?",
        a="An `async void` method cannot be awaited, so the caller cannot know when it finishes, and any exception it throws is posted to the synchronization context and crashes the process instead of being catchable. It also breaks unit testing and composition. Use `async Task`; `async void` exists only for event handlers.",
        why="One of the most common async pitfalls reviewers look for.",
        ex="""```
async void Save()      { await _repo.SaveAsync(); }   // exception crashes the app
async Task SaveAsync() { await _repo.SaveAsync(); }   // awaitable, catchable
private async void Button_Click(object s, EventArgs e) { await SaveAsync(); }  // acceptable
```""",
        src="https://learn.microsoft.com/archive/msdn-magazine/2013/march/async-await-best-practices-in-asynchronous-programming",
    ),
    dict(
        id="A05", tags=ASYNC,
        q="What does `ConfigureAwait(false)` do, and when does it matter?",
        a="By default `await` captures the current `SynchronizationContext` (UI thread, classic ASP.NET) and resumes the continuation there. `ConfigureAwait(false)` says \"resume on any thread-pool thread\", avoiding deadlocks and the cost of marshalling back. Use it in library code; it is unnecessary in ASP.NET Core (which has no synchronization context) and wrong in UI code that touches controls after the await.",
        why="Standard senior question; knowing ASP.NET Core has no context separates experienced candidates.",
        ex="""```
// Library:  var n = await stream.ReadAsync(buffer).ConfigureAwait(false);
// WPF:      var data = await LoadAsync(); label.Text = data;   // needs the UI context
```""",
        src="https://devblogs.microsoft.com/dotnet/configureawait-faq/",
    ),
    dict(
        id="A06", tags=ASYNC,
        q="How does calling `.Result` or `.Wait()` on a task cause a deadlock?",
        a="In a context that allows only one thread (UI, classic ASP.NET), `.Result` blocks that thread while waiting for the task. The awaited task's continuation needs the same thread to complete, so each waits on the other forever. Fix: await all the way up (\"async all the way\"), and in libraries use `ConfigureAwait(false)`. Even where it does not deadlock, blocking wastes a thread.",
        why="Classic interview scenario; proves you understand synchronization-context capture.",
        ex="""```
// WPF button click:
var data = LoadAsync().Result;   // deadlock: continuation needs the UI thread that is blocked here
async Task<string> LoadAsync() => await http.GetStringAsync(url);
// Fix: var data = await LoadAsync();
```""",
        src="https://learn.microsoft.com/archive/msdn-magazine/2013/march/async-await-best-practices-in-asynchronous-programming",
    ),
    dict(
        id="A07", tags=ASYNC,
        q="What is `ValueTask<T>`, and when should you prefer it over `Task<T>`?",
        a="`ValueTask<T>` is a struct that holds either a result directly or a `Task<T>`. When a method usually completes synchronously (for example a cache hit), returning `ValueTask<T>` avoids allocating a `Task` object. Trade-offs: it may be awaited only once, must not be stored or awaited concurrently, and is slightly more expensive when the operation really is asynchronous. Default to `Task<T>`; use `ValueTask<T>` in measured hot paths.",
        why="Shows performance awareness and knowledge of API contracts.",
        ex="""```
public ValueTask<User> GetAsync(int id)
    => _cache.TryGetValue(id, out var u) ? new ValueTask<User>(u) : new ValueTask<User>(LoadAsync(id));
```""",
        src="https://devblogs.microsoft.com/dotnet/understanding-the-whys-whats-and-whens-of-valuetask/",
    ),
    dict(
        id="A08", tags=ASYNC,
        q="How does cooperative cancellation with `CancellationToken` work?",
        a="A `CancellationTokenSource` owns the state and hands out a `CancellationToken` that you pass down every async call. Callees either poll `token.IsCancellationRequested`, call `token.ThrowIfCancellationRequested()` (throws `OperationCanceledException`), or forward the token to framework APIs. Cancellation is cooperative: nothing is aborted forcibly. ASP.NET Core binds `HttpContext.RequestAborted` to a `CancellationToken` action parameter automatically.",
        why="Required for responsive services, timeouts, and releasing resources when clients disconnect.",
        ex="""```
[HttpGet]
public async Task<IActionResult> Get(CancellationToken ct)
{
    var items = await _db.Items.ToListAsync(ct);   // query is cancelled if the client disconnects
    return Ok(items);
}
```""",
        src="https://learn.microsoft.com/dotnet/standard/threading/cancellation-in-managed-threads",
    ),
    dict(
        id="A09", tags=ASYNC,
        q="What does the `lock` statement do, what should you lock on, and how do `Mutex` and `SemaphoreSlim` differ from it?",
        a="`lock (obj)` compiles to `Monitor.Enter`/`Monitor.Exit` inside try/finally, letting one thread at a time into the critical section (re-entrant for the same thread). Lock on a private `readonly object` (or `System.Threading.Lock` in .NET 9+), never on `this`, a string or a `Type`. A `Mutex` is a kernel object that works across processes but is slow. `SemaphoreSlim(n)` admits up to n threads and supports `WaitAsync`, making it the tool for async code — you cannot `await` inside a `lock`.",
        why="Thread-safety basics are asked at every level; the \"await inside lock\" detail is a common follow-up.",
        ex="""```
private readonly object _gate = new();
private readonly SemaphoreSlim _sem = new(1, 1);
void Add(int x) { lock (_gate) { _list.Add(x); } }
async Task AddAsync(int x)
{
    await _sem.WaitAsync();
    try { await _repo.AddAsync(x); } finally { _sem.Release(); }
}
```""",
        src="https://learn.microsoft.com/dotnet/csharp/language-reference/statements/lock",
    ),
    dict(
        id="A10", tags=ASYNC,
        q="How do you make a shared counter thread-safe: `Interlocked`, `volatile` or `lock`?",
        a="`counter++` is three operations (read, add, write) and is not atomic. `Interlocked.Increment(ref counter)` performs it atomically with a single CPU instruction — the fastest choice for simple numeric updates. `volatile` only prevents caching and reordering of individual reads and writes; it does not make compound operations atomic. `lock` is the general tool when several fields must change together. For maps, use `ConcurrentDictionary` instead of `lock` plus `Dictionary`.",
        why="The classic \"is this code thread-safe?\" question; `volatile` is the usual wrong answer.",
        ex="""```
private int _hits;
public void Hit() => Interlocked.Increment(ref _hits);

private readonly ConcurrentDictionary<string, int> _counts = new();
public void Count(string key) => _counts.AddOrUpdate(key, 1, (_, v) => v + 1);
```""",
        src="https://learn.microsoft.com/dotnet/api/system.threading.interlocked",
    ),
    dict(
        id="A11", tags=ASYNC,
        q="How do you run several async operations concurrently, and what is the difference between `Task.WhenAll` and `Task.WhenAny`?",
        a="Start all operations first (call the methods without awaiting), then `await Task.WhenAll(tasks)` to wait for every one; it returns the results as an array and, if several fail, throws the first exception while each task still carries its own. `Task.WhenAny` completes when the first task finishes — used for timeouts or racing sources. Awaiting each call in sequence runs them one after another.",
        why="Shows you can get real concurrency from async code without extra threads.",
        ex="""```
var userTask  = _users.GetAsync(id);
var orderTask = _orders.GetAsync(id);
await Task.WhenAll(userTask, orderTask);          // both in flight at once
var (user, orders) = (await userTask, await orderTask);
```""",
        src="https://learn.microsoft.com/dotnet/api/system.threading.tasks.task.whenall",
    ),
    # ---------------------------------------------------------- asp.net core
    dict(
        id="W01", tags=WEB,
        q="What is middleware in ASP.NET Core, and how is the request pipeline built?",
        a="Middleware is a component that receives the `HttpContext`, can do work before and after calling the next component, and may short-circuit the pipeline. Components are registered in order on `WebApplication` with `Use` (calls next), `Run` (terminal), `Map` (branch by path) or `UseMiddleware<T>`; each request flows down the chain and the response flows back up. Kestrel is the web server that hands requests to the pipeline.",
        why="The architectural backbone of ASP.NET Core; routing, auth, static files and exception handling are all middleware.",
        ex="""```
app.Use(async (ctx, next) =>
{
    var sw = Stopwatch.StartNew();
    await next(ctx);                                   // run the rest of the pipeline
    logger.LogInformation("{Path} took {Ms} ms", ctx.Request.Path, sw.ElapsedMilliseconds);
});
app.MapGet("/health", () => "ok");                     // terminal endpoint
```""",
        src="https://learn.microsoft.com/aspnet/core/fundamentals/middleware/",
    ),
    dict(
        id="W02", tags=WEB,
        q="Why does middleware order matter, and what is the recommended order?",
        a="Each middleware only sees requests that earlier components pass along, so order defines behavior: exception handling goes first to catch everything below it, `UseRouting` must precede `UseAuthentication`/`UseAuthorization` so the matched endpoint is known, authentication must precede authorization, and endpoints (`MapControllers`) come last. Put `UseAuthorization` before `UseAuthentication` and the user is never identified, so every `[Authorize]` endpoint returns 401.",
        why="A practical question that reveals whether you have debugged a real pipeline.",
        ex="""```
app.UseExceptionHandler();
app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.UseCors();
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();
```""",
        src="https://learn.microsoft.com/aspnet/core/fundamentals/middleware/#middleware-order",
    ),
    dict(
        id="W03", tags=WEB,
        q="What are the DI service lifetimes in ASP.NET Core, and what is a captive dependency?",
        a="Transient: a new instance every time it is resolved. Scoped: one instance per scope, which is one per HTTP request. Singleton: one instance for the whole application. A captive dependency occurs when a longer-lived service (singleton) holds a shorter-lived one (a scoped `DbContext`), effectively making it a singleton and causing shared-state and thread-safety bugs; scope validation throws for this in the Development environment.",
        why="The single most asked ASP.NET Core question; the captive-dependency follow-up separates levels.",
        ex="""```
builder.Services.AddSingleton<ICache, MemoryCache>();
builder.Services.AddScoped<AppDbContext>();
builder.Services.AddTransient<IEmailSender, SmtpSender>();
// Bug: AddSingleton<ReportService>() where ReportService injects AppDbContext → captive dependency
```""",
        src="https://learn.microsoft.com/aspnet/core/fundamentals/dependency-injection#service-lifetimes",
    ),
    dict(
        id="W04", tags=WEB,
        q="What is the difference between middleware and filters in ASP.NET Core MVC, and which filter types exist?",
        a="Middleware runs for every request and knows nothing about MVC (no action, model or result). Filters run inside the MVC action pipeline after routing, can see the controller, action arguments and result, and can be applied per action, per controller or globally. In order: authorization, resource, action (around model binding and execution), exception, and result filters. Use middleware for cross-cutting HTTP concerns (logging, auth, CORS) and filters for MVC-specific concerns (validation, result shaping).",
        why="Shows you know where cross-cutting logic belongs and how the MVC pipeline nests inside the middleware pipeline.",
        ex="""```
public class ValidateModelFilter : IActionFilter
{
    public void OnActionExecuting(ActionExecutingContext ctx)
    {
        if (!ctx.ModelState.IsValid) ctx.Result = new BadRequestObjectResult(ctx.ModelState);
    }
    public void OnActionExecuted(ActionExecutedContext ctx) { }
}
```""",
        src="https://learn.microsoft.com/aspnet/core/mvc/controllers/filters",
    ),
    dict(
        id="W05", tags=WEB,
        q="What is the difference between attribute routing and conventional routing?",
        a="Conventional routing defines URL patterns centrally (`{controller=Home}/{action=Index}/{id?}`) and maps them by naming convention, typical for MVC views. Attribute routing puts the template on the controller and action (`[Route(\"api/[controller]\")]`, `[HttpGet(\"{id:int}\")]`); it is required by `[ApiController]` and standard for REST APIs because each endpoint's URL and constraints are explicit. Both are resolved by endpoint routing in `UseRouting`.",
        why="Routing questions test whether you can design clean REST URLs and use route constraints.",
        ex="""```
[ApiController, Route("api/orders")]
public class OrdersController : ControllerBase
{
    [HttpGet("{id:int}")]        public IActionResult Get(int id)   => ...;
    [HttpGet("{id:int}/items")]  public IActionResult Items(int id) => ...;
}
```""",
        src="https://learn.microsoft.com/aspnet/core/mvc/controllers/routing",
    ),
    dict(
        id="W06", tags=WEB,
        q="How does model binding work in ASP.NET Core, and how is validation performed?",
        a="Model binding maps request data to action parameters, checking route values, query string and form fields by default, or a source you force with `[FromRoute]`, `[FromQuery]`, `[FromBody]`, `[FromHeader]`, `[FromForm]` or `[FromServices]`. After binding, validation runs data annotations (`[Required]`, `[Range]`, `[EmailAddress]`) and `IValidatableObject`, populating `ModelState`. With `[ApiController]` an invalid state automatically returns `400` with `ValidationProblemDetails`.",
        why="Everyday API work; the follow-up is usually how you handle complex validation (FluentValidation, custom attributes).",
        ex="""```
public record CreateUserDto([Required, EmailAddress] string Email, [Range(18, 120)] int Age);

[HttpPost]
public IActionResult Create([FromBody] CreateUserDto dto) { ... }   // 400 automatically if invalid
```""",
        src="https://learn.microsoft.com/aspnet/core/mvc/models/model-binding",
    ),
    dict(
        id="W07", tags=WEB,
        q="What does the `[ApiController]` attribute do?",
        a="It turns on Web API conventions for a controller: attribute routing becomes required, an invalid `ModelState` automatically returns `400` with `ValidationProblemDetails`, complex-type parameters are inferred as `[FromBody]` (simple ones from route or query), `IFormFile` parameters as `[FromForm]`, and error responses use RFC 7807 problem details. Without it you must check `ModelState.IsValid` yourself.",
        why="A small attribute that is frequently asked about; shows you know why API controllers behave differently from MVC ones.",
        ex="""```
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    [HttpPost] public ActionResult<Product> Create(ProductDto dto) => ...;   // dto from body, auto-400
}
```""",
        src="https://learn.microsoft.com/aspnet/core/web-api/#apicontroller-attribute",
    ),
    dict(
        id="W08", tags=WEB,
        q="What is the difference between returning `IActionResult`, `ActionResult<T>` and a plain type from an action?",
        a="Returning `T` directly serializes it with `200` but cannot express other status codes. `IActionResult` lets you return any result (`Ok()`, `NotFound()`, `BadRequest()`) but hides the payload type from OpenAPI tooling. `ActionResult<T>` combines both: implicit conversions from `T` and from any `ActionResult`, so tooling knows the success type while you keep full status control. Prefer `ActionResult<T>` in Web APIs.",
        why="Shows you care about API contracts and generated clients, not just \"it works\".",
        ex="""```
[HttpGet("{id}")]
public async Task<ActionResult<Product>> Get(int id)
{
    var p = await _repo.FindAsync(id);
    return p is null ? NotFound() : p;     // both convert implicitly
}
```""",
        src="https://learn.microsoft.com/aspnet/core/web-api/action-return-types",
    ),
    dict(
        id="W09", tags=WEB,
        q="How does configuration work in ASP.NET Core, and in what order do sources override each other?",
        a="`IConfiguration` merges key/value pairs from many providers, and later providers override earlier ones. Default order for `WebApplication.CreateBuilder`: `appsettings.json` → `appsettings.{Environment}.json` → user secrets (Development only) → environment variables → command-line arguments. Keys are hierarchical (`Logging:LogLevel:Default`; use `__` instead of `:` in environment variables). The environment comes from `ASPNETCORE_ENVIRONMENT` or `DOTNET_ENVIRONMENT`.",
        why="Explains why a production environment variable silently beats appsettings and how to keep secrets out of source control.",
        ex="Setting the environment variable `ConnectionStrings__Default=Server=prod;...` overrides `\"ConnectionStrings\": { \"Default\": \"...\" }` from appsettings.json.",
        src="https://learn.microsoft.com/aspnet/core/fundamentals/configuration/",
    ),
    dict(
        id="W10", tags=WEB,
        q="What is the Options pattern, and how do `IOptions<T>`, `IOptionsSnapshot<T>` and `IOptionsMonitor<T>` differ?",
        a="The Options pattern binds a configuration section to a strongly typed class via `services.Configure<T>(config.GetSection(\"X\"))` and injects it into consumers. `IOptions<T>` is a singleton computed once at first use and never reloaded. `IOptionsSnapshot<T>` is scoped and recomputed per request, so it picks up file changes, but it cannot be injected into singletons. `IOptionsMonitor<T>` is a singleton exposing `CurrentValue` and `OnChange` — use it in singletons or background services that need live updates.",
        why="Very common follow-up to the configuration question; \"which one in a singleton\" is the trap.",
        ex="""```
builder.Services.Configure<SmtpOptions>(builder.Configuration.GetSection("Smtp"));

public class Mailer(IOptionsMonitor<SmtpOptions> opts)
{
    public void Send() => Connect(opts.CurrentValue.Host);
}
```""",
        src="https://learn.microsoft.com/aspnet/core/fundamentals/configuration/options",
    ),
    dict(
        id="W11", tags=WEB,
        q="What is the difference between authentication and authorization in ASP.NET Core, and how are schemes and policies used?",
        a="Authentication establishes who the caller is: an authentication scheme (cookie, JWT bearer, OpenID Connect) turns credentials into a `ClaimsPrincipal` on `HttpContext.User`. Authorization decides what that principal may do: `[Authorize]` requires an authenticated user, and roles (`Roles = \"Admin\"`) or policies (`Policy = \"CanEdit\"`, built from requirements and handlers) add rules. `UseAuthentication()` must run before `UseAuthorization()`.",
        why="Foundational security question; policies vs. roles is the typical follow-up.",
        ex="""```
builder.Services.AddAuthorization(o => o.AddPolicy("Over18",
    p => p.RequireAssertion(c => int.TryParse(c.User.FindFirst("age")?.Value, out var a) && a >= 18)));

[Authorize(Policy = "Over18")]
public IActionResult Buy() => ...;
```""",
        src="https://learn.microsoft.com/aspnet/core/security/authorization/introduction",
    ),
    dict(
        id="W12", tags=WEB,
        q="How does JWT bearer authentication work in an ASP.NET Core API?",
        a="The client authenticates once (login endpoint or identity provider) and receives a JSON Web Token: a signed, base64url-encoded `header.payload.signature` carrying claims and an expiry. It sends it on each request as `Authorization: Bearer <token>`. The JWT bearer handler validates the signature (shared key or the issuer's public keys), issuer, audience and lifetime, then builds the `ClaimsPrincipal` — no server-side session is needed. Short-lived access tokens plus refresh tokens limit the damage of a leaked token, since JWTs cannot be revoked without extra state.",
        why="Standard for stateless APIs and microservices; interviewers probe validation parameters and revocation trade-offs.",
        ex="""```
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(o => o.TokenValidationParameters = new()
    {
        ValidIssuer = "https://auth.example.com",
        ValidAudience = "my-api",
        IssuerSigningKey = new SymmetricSecurityKey(key),
        ValidateLifetime = true
    });
```""",
        src="https://learn.microsoft.com/aspnet/core/security/authentication/configure-jwt-bearer-authentication",
    ),
    dict(
        id="W13", tags=WEB,
        q="What is CORS, and how do you enable it in ASP.NET Core?",
        a="Cross-Origin Resource Sharing is a browser mechanism: scripts on one origin (scheme + host + port) cannot read responses from another unless the server opts in with `Access-Control-Allow-*` headers; non-simple requests trigger a preflight `OPTIONS` call. In ASP.NET Core, register a policy with `AddCors`, add `UseCors()` after `UseRouting` and before `UseAuthorization`, and restrict origins, headers and methods (`AllowAnyOrigin` cannot be combined with credentials). CORS protects browsers only: server-to-server calls ignore it.",
        why="Every SPA + API developer has hit a CORS error; interviewers check you understand it is enforced by the browser, not the API.",
        ex="""```
builder.Services.AddCors(o => o.AddPolicy("spa", p =>
    p.WithOrigins("https://app.example.com").AllowAnyHeader().AllowAnyMethod()));
app.UseCors("spa");
```""",
        src="https://learn.microsoft.com/aspnet/core/security/cors",
    ),
    dict(
        id="W14", tags=WEB,
        q="Why should you use `IHttpClientFactory` instead of `new HttpClient()`?",
        a="Creating an `HttpClient` per request exhausts sockets (connections linger in TIME_WAIT), while one static instance never picks up DNS changes. `IHttpClientFactory` pools and recycles the underlying `HttpMessageHandler` (default lifetime two minutes), giving both connection reuse and DNS refresh. It also supports named and typed clients with central configuration, plus delegating handlers for retries, auth headers and logging (Polly or `AddStandardResilienceHandler`).",
        why="A well-known production pitfall; expected knowledge for anyone writing service-to-service calls.",
        ex="""```
builder.Services.AddHttpClient<WeatherClient>(c => c.BaseAddress = new Uri("https://api.weather.com"))
    .AddStandardResilienceHandler();

public class WeatherClient(HttpClient http)
{
    public Task<string> GetTodayAsync() => http.GetStringAsync("/today");
}
```""",
        src="https://learn.microsoft.com/aspnet/core/fundamentals/http-requests",
    ),
    dict(
        id="W15", tags=WEB,
        q="How do you handle exceptions globally in an ASP.NET Core API?",
        a="Register `app.UseExceptionHandler()` as the first middleware so it catches anything thrown downstream, and implement `IExceptionHandler` (.NET 8+) to map exceptions to responses; add `AddProblemDetails()` so errors come back as RFC 7807 `ProblemDetails` JSON. In Development, `UseDeveloperExceptionPage` shows stack traces. Avoid try/catch in every action: let exceptions bubble to the handler, log once there, and never leak internals to clients.",
        why="Shows you can produce a consistent error contract and avoid duplicated handling.",
        ex="""```
public class AppExceptionHandler : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(HttpContext ctx, Exception ex, CancellationToken ct)
    {
        ctx.Response.StatusCode = ex is NotFoundException ? 404 : 500;
        await ctx.Response.WriteAsJsonAsync(new ProblemDetails { Title = ex.Message }, ct);
        return true;
    }
}
builder.Services.AddExceptionHandler<AppExceptionHandler>();
builder.Services.AddProblemDetails();
app.UseExceptionHandler();
```""",
        src="https://learn.microsoft.com/aspnet/core/fundamentals/error-handling",
    ),
    dict(
        id="W16", tags=WEB,
        q="How does logging work in ASP.NET Core, and what is structured logging?",
        a="`ILogger<T>` is injected anywhere and writes to every registered provider (Console, Debug, EventLog, Application Insights, Serilog, OpenTelemetry). Levels from Trace to Critical are filtered per category through configuration (`Logging:LogLevel`). Structured logging means using message templates with named placeholders instead of string interpolation, so each value is stored as a searchable property rather than flattened text. Pass exceptions as the first argument (`LogError(ex, ...)`).",
        why="Interviewers look for `{OrderId}` templates over `$\"...\"` and for sensible production log levels.",
        ex="""```
_logger.LogInformation("Order {OrderId} placed by {UserId} for {Total}", order.Id, user.Id, order.Total);
// Not: _logger.LogInformation($"Order {order.Id} placed...");  // loses structure, formats even when filtered out
```""",
        src="https://learn.microsoft.com/aspnet/core/fundamentals/logging/",
    ),
    dict(
        id="W17", tags=WEB,
        q="How do you run background work in ASP.NET Core (`IHostedService` / `BackgroundService`)?",
        a="Implement `IHostedService` or derive from `BackgroundService`, override `ExecuteAsync(CancellationToken)`, and register it with `AddHostedService<T>()`. The host starts it with the app and signals the token on shutdown. Hosted services are singletons, so to use scoped services such as `DbContext`, create a scope with `IServiceScopeFactory`. Handle exceptions inside the loop: since .NET 6 an unhandled exception stops the host. For producer/consumer work, pair it with `Channel<T>`.",
        why="Common for scheduled jobs, queue consumers and cache warm-up; the scoped-service trap is the follow-up.",
        ex="""```
public class CleanupWorker(IServiceScopeFactory scopes) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken ct)
    {
        while (!ct.IsCancellationRequested)
        {
            using var scope = scopes.CreateScope();
            await scope.ServiceProvider.GetRequiredService<AppDbContext>().PurgeExpiredAsync(ct);
            await Task.Delay(TimeSpan.FromMinutes(5), ct);
        }
    }
}
```""",
        src="https://learn.microsoft.com/aspnet/core/fundamentals/host/hosted-services",
    ),
]
