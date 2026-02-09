# Web Gateway Design

The web gateway is designed to provide safe and controlled access to the web for the swarm. It consists of the following components:

* WebGateway: The main class that handles request validation and forwarding.
* GitValidator: Validates git operations to ensure only allowed operations are performed.
* RequestAllowlist: Manages the allowlist of domains and URL patterns.
* AuditLogger: Logs all requests for auditing and monitoring purposes.
* RateLimiter: Limits the number of requests per minute to prevent abuse.

The web gateway works as follows:

1. A request is received by the WebGateway class.
2. The request is validated using the RequestAllowlist and GitValidator classes.
3. If the request is allowed, it is forwarded to the destination.
4. The request is logged by the AuditLogger class.
5. The RateLimiter class checks if the request is allowed based on the rate limit.

The web gateway provides a safe and controlled way for the swarm to access the web, while preventing malicious activities such as credential exfiltration and unauthorized access to external services.