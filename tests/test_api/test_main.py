"""Tests para los endpoints principales de la API"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestRootEndpoint:
    """Tests para el endpoint raíz"""
    
    def test_root_returns_200(self):
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_returns_json(self):
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"
    
    def test_root_contains_message(self):
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert "HelioBio" in data["message"]


class TestSolarActivity:
    """Tests para el endpoint de actividad solar"""
    
    def test_solar_activity_returns_200(self):
        response = client.get("/solar/activity")
        assert response.status_code == 200
    
    def test_solar_activity_returns_list(self):
        response = client.get("/solar/activity")
        data = response.json()
        assert isinstance(data, list)
    
    def test_solar_activity_with_dates(self):
        response = client.get("/solar/activity?start_date=2020-01-01&end_date=2020-12-31")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
    
    def test_solar_activity_has_required_fields(self):
        response = client.get("/solar/activity?start_date=2023-01-01&end_date=2023-06-30")
        data = response.json()
        assert len(data) > 0
        item = data[0]
        required_fields = ["date", "sunspot_number", "classification"]
        for field in required_fields:
            assert field in item, f"Falta el campo {field}"


class TestHealthEvents:
    """Tests para el endpoint de eventos de salud"""
    
    def test_health_events_returns_200(self):
        response = client.get("/health/events")
        assert response.status_code == 200
    
    def test_health_events_returns_list(self):
        response = client.get("/health/events")
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_health_events_has_required_fields(self):
        response = client.get("/health/events")
        data = response.json()
        event = data[0]
        required_fields = ["name", "start_year", "end_year", "notes"]
        for field in required_fields:
            assert field in event, f"Falta el campo {field}"
    
    def test_health_events_includes_covid(self):
        response = client.get("/health/events")
        data = response.json()
        names = [e["name"] for e in data]
        assert any("COVID" in name or "covid" in name for name in names)


class TestChizhevskyKnowledge:
    """Tests para el endpoint de conocimiento de Chizhevsky"""
    
    def test_knowledge_returns_200(self):
        response = client.get("/chizhevsky/knowledge")
        assert response.status_code == 200
    
    def test_knowledge_has_solar_cycles(self):
        response = client.get("/chizhevsky/knowledge")
        data = response.json()
        assert "solar_cycles" in data
        assert "duration" in data["solar_cycles"]
    
    def test_knowledge_has_phases(self):
        response = client.get("/chizhevsky/knowledge")
        data = response.json()
        phases = data["solar_cycles"]["phases"]
        expected_phases = ["minimum", "organizing", "maximum", "declining"]
        for phase in expected_phases:
            assert phase in phases, f"Falta la fase {phase}"
    
    def test_knowledge_has_historical_correlations(self):
        response = client.get("/chizhevsky/knowledge")
        data = response.json()
        assert "historical_correlations" in data
        assert "1918" in data["historical_correlations"]


class TestAnalysisCorrelate:
    """Tests para el endpoint de análisis de correlación"""
    
    def test_correlate_returns_200(self):
        response = client.get("/analysis/correlate")
        assert response.status_code == 200
    
    def test_correlate_has_correlation_score(self):
        response = client.get("/analysis/correlate")
        data = response.json()
        assert "correlation_score" in data
        assert isinstance(data["correlation_score"], (int, float))
    
    def test_correlate_has_graph(self):
        response = client.get("/analysis/correlate")
        data = response.json()
        assert "graph_image_base64" in data
        assert len(data["graph_image_base64"]) > 100
    
    def test_correlate_has_predictions(self):
        response = client.get("/analysis/correlate")
        data = response.json()
        assert "prediction" in data
        assert "current_risk_level" in data["prediction"]
    
    def test_correlate_with_custom_params(self):
        response = client.get(
            "/analysis/correlate?event_type=pandemics&years_before=5&years_after=3"
        )
        assert response.status_code == 200
