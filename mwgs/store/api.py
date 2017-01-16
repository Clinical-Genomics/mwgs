# -*- coding: utf-8 -*-
from sqlservice import SQLClient

from .models import Model


def connect(db_uri):
    """Connect to database."""
    db = SQLClient({'SQL_DATABASE_URI': db_uri}, model_class=Model)
    return db


def connect_app(app):
    """Connect Flask application."""
    db = connect(app.config['SQL_DATABASE_URI'])
    return db


def build_sample(data):
    """Prepare data to match database interface."""
    parsed = {
        'lims_id': data['Sample Name'],
        'name': data['External Name'],
        'project_id': data['Project'],
        'reference_genome': data['Reference Genome'],
        'total_reads': data['Total Reads'],
        'insert_size': data['Median Insert Size'],
        'duplication_rate': data['Duplication Rate'],
        'mapped_rate': data['Fraction aligned to Reference'],
        'coverage_10x': data['Fraction of bases with cov >= 10X'],
    }
    return parsed


def project(db, project_id):
    query = db.Sample.filter_by(project_id=project_id)
    return query


def plot_data(samples, datafield):
    """Calculate time it takes to analyze a sample."""
    points = [{
        'name': sample.lims_id,
        'y': getattr(sample, datafield),
    } for sample in samples]
    return points


def plot_reads_coverage(samples):
    """Plot Total reads vs. Coverage 10x."""
    points = [{
        'name': sample.lims_id,
        'y': sample.coverage_10x,
        'x': sample.total_reads,
    } for sample in samples]
    return points
