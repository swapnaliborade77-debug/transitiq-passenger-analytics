# Public Transport and Passenger Traffic Analytics

A college mini project demonstrating CSV loading, cleaning, interactive visualizations, and SQL data modeling.

**Dataset note:** the bundled dataset is synthetic demonstration data, not official transport data.

## Run on Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```
Open the local URL shown by Streamlit, usually http://localhost:8501.

If activation is blocked:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Run tests
```powershell
pytest
```

## Optional MySQL
1. Install MySQL Server and MySQL Workbench.
2. Run `database/schema.sql`.
3. Import the CSV into `transport_records`, mapping `date` to `service_date` and `hour` to `hour_of_day`.
4. Run `database/sample_queries.sql`.

The dashboard reads CSV and does not require MySQL to start. Never commit real passwords.

## Dataset columns
- `route`: sample route identifier
- `stop`: sample stop name
- `date`: sample service date
- `hour`: hour from 0 to 23
- `passengers`: synthetic count for demonstration
- `vehicle_capacity`: illustrative capacity field, not matched trip-level occupancy data

Use real public data only after checking the source and licence. Passenger-demand analysis requires actual ridership counts.
