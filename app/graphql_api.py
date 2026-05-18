"""API GraphQL para HelioBio-API"""
import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional
from datetime import datetime

# Schemas GraphQL
@strawberry.type
class SolarActivityGQL:
    date: str
    sunspot_number: float
    classification: str
    flare_activity: Optional[float] = 0.0
    geomagnetic_storm: Optional[float] = 0.0

@strawberry.type
class PandemicGQL:
    name: str
    start_year: int
    end_year: int
    death_count: Optional[int] = None
    solar_correlation: Optional[float] = None

@strawberry.type
class CorrelationResultGQL:
    correlation_score: float
    p_value: float
    risk_level: str
    period: str

@strawberry.type
class Query:
    @strawberry.field
    async def solar_activity(self, start_date: str = "2024-01-01", end_date: str = "2024-12-31") -> List[SolarActivityGQL]:
        """Obtiene actividad solar vía GraphQL"""
        from app.main import fetch_solar_data
        df = await fetch_solar_data(start_date, end_date)
        records = df.to_dict('records')
        return [
            SolarActivityGQL(
                date=str(r['date'])[:10],
                sunspot_number=float(r['sunspot_number']),
                classification=str(r['classification']),
                flare_activity=float(r.get('flare_activity', 0)),
                geomagnetic_storm=float(r.get('geomagnetic_storm', 0))
            )
            for r in records[-10:]
        ]
    
    @strawberry.field
    async def pandemics(self) -> List[PandemicGQL]:
        """Obtiene pandemias vía GraphQL"""
        from app.pandemic_data import get_pandemic_data
        df = get_pandemic_data()
        records = df.to_dict('records')
        return [
            PandemicGQL(
                name=r['name'],
                start_year=int(r['start_year']),
                end_year=int(r['end_year']),
                death_count=r.get('death_count'),
                solar_correlation=r.get('solar_correlation')
            )
            for r in records
        ]
    
    @strawberry.field
    async def correlation(self, years_before: int = 10, years_after: int = 5) -> CorrelationResultGQL:
        """Análisis de correlación vía GraphQL"""
        from app.main import fetch_solar_data, get_epidemiological_data, advanced_correlation_analysis, predict_next_events
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - __import__('datetime').timedelta(days=365*(years_before+years_after))).strftime("%Y-%m-%d")
        solar_df = await fetch_solar_data(start_date, end_date)
        events_df = get_epidemiological_data()
        event_dates = [datetime(year, 6, 15) for year in events_df["start_year"]]
        analysis = advanced_correlation_analysis(solar_df, event_dates)
        prediction = predict_next_events(solar_df, analysis)
        
        return CorrelationResultGQL(
            correlation_score=float(analysis['pearson_correlation']),
            p_value=float(analysis['p_value']),
            risk_level=str(prediction.get('current_risk_level', 'N/A')),
            period=f"{solar_df['date'].min().strftime('%Y-%m')} a {solar_df['date'].max().strftime('%Y-%m')}"
        )

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)
