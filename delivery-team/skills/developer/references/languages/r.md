# R Best Practices

Version baseline: R 4.x (current stable). Tidyverse-aware; base R alternatives noted where relevant.

## Style & Formatting

- Follow the [tidyverse style guide](https://style.tidyverse.org/): `snake_case` for variables and functions, `PascalCase` for R6 classes
- Use `<-` for assignment, not `=` (except in function arguments)
- Limit lines to 80 characters; use `styler` to auto-format
- One statement per line; no semicolons
- Use `lintr` for static analysis; enforce in CI with `lintr::lint_package()`
- Spaces around `<-`, `=`, operators; space after commas; no space before `(`
- Use `TRUE` / `FALSE`, not `T` / `F` (T and F can be overwritten)
- Comment with `#` followed by a space; use `# ----` section markers for navigation

## Idioms & Patterns

- Prefer vectorized operations over explicit loops:
  ```r
  # Preferred
  x <- c(1, 2, 3)
  result <- x * 2

  # Avoid unless necessary
  result <- vector("numeric", length(x))
  for (i in seq_along(x)) result[i] <- x[i] * 2
  ```
- Use `seq_along(x)` and `seq_len(n)` instead of `1:length(x)` or `1:n` (avoids zero-length sequence bugs)
- Use `vapply()` over `sapply()` for type-safe results: `vapply(x, f, numeric(1))`
- Use `lapply()` / `vapply()` over `for` when building lists or vectors from iteration
- Use pipe operator `|>` (base R, R 4.1+) or `%>%` (magrittr/dplyr) consistently; pick one per project
- Use `\(x)` lambda syntax (R 4.1+) for anonymous functions: `lapply(x, \(i) i^2)`
- Prefer `switch()` over long `if/else if` chains for dispatch on string values
- Use `match.arg()` for function argument validation:
  ```r
  my_fun <- function(method = c("pearson", "spearman", "kendall")) {
    method <- match.arg(method)
    ...
  }
  ```

## Tidyverse Patterns

- Use `dplyr` for data manipulation (`filter`, `mutate`, `summarise`, `group_by`, `join_*`)
- Use `tidyr` for reshaping (`pivot_longer`, `pivot_wider`, `unnest`)
- Use `purrr` for functional programming (`map`, `map_dbl`, `walk`, `reduce`) in place of `*apply` in tidyverse workflows
- Use `ggplot2` for visualization — build plots in layers; name aesthetics explicitly
- Use `readr` for file I/O (faster, returns tibbles, better type inference than `read.csv`)
- Use `tibble` over `data.frame`: prints cleanly, no row names, no string-to-factor coercion
- Do not modify global state inside dplyr verbs or purrr map calls

## Project Structure

- Use `{renv}` for reproducible package environments — always include `renv.lock` in version control
- Organize projects as R packages or with a standard layout:
  ```
  project/
  ├── R/             # source files — one function per file, file named after function
  ├── tests/testthat/
  ├── data/          # raw data (read-only)
  ├── data-raw/      # scripts to produce data/
  ├── vignettes/     # long-form documentation
  ├── DESCRIPTION    # if building a package
  └── renv.lock
  ```
- Name R files after their primary function or topic: `clean_data.R`, `model_training.R`
- Use `here::here()` for file paths — never `setwd()` or hardcoded absolute paths

## Error Handling

- Use `tryCatch()` for recoverable errors:
  ```r
  result <- tryCatch(
    expr = { risky_operation() },
    error = function(e) { message("Error: ", conditionMessage(e)); NULL },
    warning = function(w) { message("Warning: ", conditionMessage(w)); NULL }
  )
  ```
- Use `withCallingHandlers()` when you need to log and continue (does not exit like `tryCatch`)
- Use `stop()` with a descriptive message for unrecoverable errors in functions
- Use `warning()` for recoverable problems; use `message()` for informational output (both suppress-able)
- Validate function inputs early: `stopifnot()` for simple conditions; `rlang::abort()` / `cli::cli_abort()` for structured errors with context
- Use `rlang::abort()` (from rlang package) for structured conditions with class-based error handling

## Testing

- Use `{testthat}` (version 3+) for all tests:
  ```r
  test_that("filter_active returns only active records", {
    df <- tibble::tibble(status = c("active", "inactive", "active"))
    result <- filter_active(df)
    expect_equal(nrow(result), 2)
    expect_true(all(result$status == "active"))
  })
  ```
- Run tests: `devtools::test()` or `testthat::test_dir("tests/testthat")`
- Use `{covr}` for code coverage: `covr::package_coverage()`
- Test edge cases: empty inputs, NA values, single-row data frames, zero-length vectors
- Use `withr` for test isolation (temporary files, env vars, options):
  ```r
  withr::with_tempdir({ ... })
  withr::local_options(list(warn = 2))
  ```

## Security

- Never embed credentials in scripts — use environment variables via `Sys.getenv("MY_SECRET")` or `{keyring}`
- Use `{httr2}` or `{httr}` for HTTP requests — they handle redirects, retries, and SSL properly
- Parameterize all database queries — never `paste()` user input into SQL strings; use `{DBI}` with `dbBind()`
- Validate and sanitize inputs when accepting external data before passing to `system()` or `system2()`
- Avoid `eval(parse(text = user_input))` — arbitrary code execution

## Performance

- Profile before optimizing: `profvis::profvis({ code })` for call-level profiling
- Use `{data.table}` for large datasets (>1M rows) where `dplyr` throughput is insufficient
- Avoid growing vectors in loops (`c(result, new_val)`) — pre-allocate with `vector("list", n)` or use `purrr::map()`
- Use `Rcpp` to move tight loops to C++ when vectorization is insufficient
- Use `{future}` + `{furrr}` for parallel computation: `furrr::future_map()` as a drop-in for `purrr::map()`
- Cache expensive computations with `{memoise}`: `memo_fn <- memoise::memoise(expensive_fn)`
- Read large files with `{arrow}` (Parquet/Feather) or `data.table::fread()` instead of `read.csv()`

## R Markdown / Quarto

- Use `{quarto}` for new documents (supersedes R Markdown for most use cases)
- Set `echo: false` and `warning: false` in production report chunks; show code in analyses
- Use chunk names for navigation and caching; cached chunks stored in `_cache/`
- Use `params:` in YAML front matter for parameterized reports
- Separate data processing scripts from reporting documents — don't embed heavy computation in .qmd/.Rmd

## Anti-Patterns to Avoid

- **`T` / `F` instead of `TRUE` / `FALSE`** — T and F can be reassigned
- **`1:length(x)` or `1:n`** — breaks when length is 0 or n is 0; use `seq_along()` / `seq_len()`
- **`sapply()` in production code** — return type unpredictable; use `vapply()` or `purrr::map_*()`
- **`attach()`** — pollutes the search path; use `with()` or explicit `df$column` access
- **`setwd()` in scripts** — breaks reproducibility; use `here::here()`
- **Modifying global state** — use function arguments and return values; avoid `<<-` except in R6/closures where intentional
- **`options(stringsAsFactors = TRUE)`** — disabled by default in R 4.x; don't re-enable it
- **Growing objects in a loop** — `result <- c(result, x)` is O(n²); pre-allocate or use `purrr`
- **Not using `renv`** — package versions drift; always lock dependencies

## Tooling

| Tool | Purpose |
|------|---------|
| `lintr` | Static analysis and style enforcement |
| `styler` | Auto-format code to tidyverse style |
| `testthat` | Unit and integration testing |
| `covr` | Code coverage measurement |
| `devtools` | Package development workflow (`load_all`, `test`, `check`) |
| `renv` | Reproducible package environments |
| `profvis` | Interactive profiling |
| `rlang` / `cli` | Structured error conditions and user messages |
| `here` | Portable file paths |
| `quarto` | Reproducible reporting and literate programming |
