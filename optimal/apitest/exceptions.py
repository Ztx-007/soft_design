class AppError(Exception):
    def __init__(self, *, message: str, status_code: int = 400, code: str = "app_error") -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code


class ExchangeRateNotFound(AppError):
    def __init__(self, from_currency: str, to_currency: str) -> None:
        super().__init__(
            message=f"Exchange rate not found for {from_currency} to {to_currency}",
            status_code=404,
            code="rate_not_found",
        )
