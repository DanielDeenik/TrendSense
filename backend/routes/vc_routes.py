from flask import Blueprint, request, jsonify, render_template, current_app
from ..models.vc import VCFirm, InvestmentThesis, Portfolio
from ..models.startup import Startup, StartupDocument
from ..models.assessment import LCAData, StartupAssessment, MaterialityMatrix
from ..database import db
import os
import json
import logging
from werkzeug.utils import secure_filename
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
vc_bp = Blueprint('vc', __name__)

# Helper function to get allowed file extensions
def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# VC Firm Routes
@vc_bp.route('/api/vc/firms', methods=['GET'])
def get_vc_firms():
    """
    Get all VC firms.
    """
    try:
        firms = VCFirm.query.all()
        return jsonify({
            'vc_firms': [firm.to_dict() for firm in firms]
        })
    except Exception as e:
        logger.error(f"Error getting VC firms: {str(e)}")
        return jsonify({'error': str(e)}), 500

@vc_bp.route('/api/vc/firms', methods=['POST'])
def create_vc_firm():
    """
    Create a new VC firm.
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400
        
        # Create new VC firm
        firm = VCFirm(
            name=data.get('name'),
            description=data.get('description'),
            website=data.get('website'),
            founded_year=data.get('founded_year'),
            headquarters=data.get('headquarters'),
            fund_size=data.get('fund_size'),
            investment_focus=data.get('investment_focus'),
            sustainability_focus=data.get('sustainability_focus'),
            impact_goals=data.get('impact_goals')
        )
        
        # Save to database
        db.session.add(firm)
        db.session.commit()
        
        return jsonify({
            'message': 'VC firm created successfully',
            'vc_firm': firm.to_dict()
        }), 201
    except Exception as e:
        logger.error(f"Error creating VC firm: {str(e)}")
        return jsonify({'error': str(e)}), 500

@vc_bp.route('/api/vc/firms/<int:firm_id>', methods=['GET'])
def get_vc_firm(firm_id):
    """
    Get a specific VC firm.
    """
    try:
        firm = VCFirm.query.get(firm_id)
        if not firm:
            return jsonify({'error': 'VC firm not found'}), 404
        
        return jsonify({
            'vc_firm': firm.to_dict()
        })
    except Exception as e:
        logger.error(f"Error getting VC firm: {str(e)}")
        return jsonify({'error': str(e)}), 500

@vc_bp.route('/api/vc/firms/<int:firm_id>', methods=['PUT'])
def update_vc_firm(firm_id):
    """
    Update a specific VC firm.
    """
    try:
        firm = VCFirm.query.get(firm_id)
        if not firm:
            return jsonify({'error': 'VC firm not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'name' in data:
            firm.name = data['name']
        if 'description' in data:
            firm.description = data['description']
        if 'website' in data:
            firm.website = data['website']
        if 'founded_year' in data:
            firm.founded_year = data['founded_year']
        if 'headquarters' in data:
            firm.headquarters = data['headquarters']
        if 'fund_size' in data:
            firm.fund_size = data['fund_size']
        if 'investment_focus' in data:
            firm.investment_focus = data['investment_focus']
        if 'sustainability_focus' in data:
            firm.sustainability_focus = data['sustainability_focus']
        if 'impact_goals' in data:
            firm.impact_goals = data['impact_goals']
        
        # Save to database
        db.session.commit()
        
        return jsonify({
            'message': 'VC firm updated successfully',
            'vc_firm': firm.to_dict()
        })
    except Exception as e:
        logger.error(f"Error updating VC firm: {str(e)}")
        return jsonify({'error': str(e)}), 500

@vc_bp.route('/api/vc/firms/<int:firm_id>', methods=['DELETE'])
def delete_vc_firm(firm_id):
    """
    Delete a specific VC firm.
    """
    try:
        firm = VCFirm.query.get(firm_id)
        if not firm:
            return jsonify({'error': 'VC firm not found'}), 404
        
        # Delete from database
        db.session.delete(firm)
        db.session.commit()
        
        return jsonify({
            'message': 'VC firm deleted successfully'
        })
    except Exception as e:
        logger.error(f"Error deleting VC firm: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Investment Thesis Routes
@vc_bp.route('/api/vc/theses', methods=['GET'])
def get_investment_theses():
    """
    Get all investment theses.
    """
    try:
        vc_firm_id = request.args.get('vc_firm_id', type=int)
        
        if vc_firm_id:
            theses = InvestmentThesis.query.filter_by(vc_firm_id=vc_firm_id).all()
        else:
            theses = InvestmentThesis.query.all()
        
        return jsonify({
            'investment_theses': [thesis.to_dict() for thesis in theses]
        })
    except Exception as e:
        logger.error(f"Error getting investment theses: {str(e)}")
        return jsonify({'error': str(e)}), 500

@vc_bp.route('/api/vc/theses', methods=['POST'])
def create_investment_thesis():
    """
    Create a new investment thesis.
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('vc_firm_id'):
            return jsonify({'error': 'VC firm ID is required'}), 400
        if not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400
        
        # Check if VC firm exists
        vc_firm = VCFirm.query.get(data['vc_firm_id'])
        if not vc_firm:
            return jsonify({'error': 'VC firm not found'}), 404
        
        # Create new investment thesis
        thesis = InvestmentThesis(
            vc_firm_id=data['vc_firm_id'],
            title=data['title'],
            description=data.get('description'),
            focus_areas=data.get('focus_areas'),
            investment_criteria=data.get('investment_criteria'),
            sustainability_priorities=data.get('sustainability_priorities'),
            regulatory_considerations=data.get('regulatory_considerations'),
            keywords=data.get('keywords')
        )
        
        # Save to database
        db.session.add(thesis)
        db.session.commit()
        
        return jsonify({
            'message': 'Investment thesis created successfully',
            'investment_thesis': thesis.to_dict()
        }), 201
    except Exception as e:
        logger.error(f"Error creating investment thesis: {str(e)}")
        return jsonify({'error': str(e)}), 500

@vc_bp.route('/api/vc/theses/<int:thesis_id>', methods=['GET'])
def get_investment_thesis(thesis_id):
    """
    Get a specific investment thesis.
    """
    try:
        thesis = InvestmentThesis.query.get(thesis_id)
        if not thesis:
            return jsonify({'error': 'Investment thesis not found'}), 404
        
        return jsonify({
            'investment_thesis': thesis.to_dict()
        })
    except Exception as e:
        logger.error(f"Error getting investment thesis: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Portfolio Routes
@vc_bp.route('/api/vc/portfolios', methods=['GET'])
def get_portfolios():
    """
    Get all portfolios.
    """
    try:
        vc_firm_id = request.args.get('vc_firm_id', type=int)
        
        if vc_firm_id:
            portfolios = Portfolio.query.filter_by(vc_firm_id=vc_firm_id).all()
        else:
            portfolios = Portfolio.query.all()
        
        return jsonify({
            'portfolios': [portfolio.to_dict() for portfolio in portfolios]
        })
    except Exception as e:
        logger.error(f"Error getting portfolios: {str(e)}")
        return jsonify({'error': str(e)}), 500

@vc_bp.route('/api/vc/portfolios', methods=['POST'])
def create_portfolio():
    """
    Create a new portfolio.
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('vc_firm_id'):
            return jsonify({'error': 'VC firm ID is required'}), 400
        if not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400
        
        # Check if VC firm exists
        vc_firm = VCFirm.query.get(data['vc_firm_id'])
        if not vc_firm:
            return jsonify({'error': 'VC firm not found'}), 404
        
        # Check if investment thesis exists if provided
        if data.get('investment_thesis_id'):
            thesis = InvestmentThesis.query.get(data['investment_thesis_id'])
            if not thesis:
                return jsonify({'error': 'Investment thesis not found'}), 404
        
        # Create new portfolio
        portfolio = Portfolio(
            vc_firm_id=data['vc_firm_id'],
            name=data['name'],
            description=data.get('description'),
            fund_name=data.get('fund_name'),
            vintage_year=data.get('vintage_year'),
            investment_thesis_id=data.get('investment_thesis_id')
        )
        
        # Save to database
        db.session.add(portfolio)
        db.session.commit()
        
        return jsonify({
            'message': 'Portfolio created successfully',
            'portfolio': portfolio.to_dict()
        }), 201
    except Exception as e:
        logger.error(f"Error creating portfolio: {str(e)}")
        return jsonify({'error': str(e)}), 500

@vc_bp.route('/api/vc/portfolios/<int:portfolio_id>', methods=['GET'])
def get_portfolio(portfolio_id):
    """
    Get a specific portfolio.
    """
    try:
        portfolio = Portfolio.query.get(portfolio_id)
        if not portfolio:
            return jsonify({'error': 'Portfolio not found'}), 404
        
        return jsonify({
            'portfolio': portfolio.to_dict()
        })
    except Exception as e:
        logger.error(f"Error getting portfolio: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Startup Routes
@vc_bp.route('/api/vc/startups', methods=['GET'])
def get_startups():
    """
    Get all startups.
    """
    try:
        portfolio_id = request.args.get('portfolio_id', type=int)
        
        if portfolio_id:
            startups = Startup.query.filter_by(portfolio_id=portfolio_id).all()
        else:
            startups = Startup.query.all()
        
        return jsonify({
            'startups': [startup.to_dict() for startup in startups]
        })
    except Exception as e:
        logger.error(f"Error getting startups: {str(e)}")
        return jsonify({'error': str(e)}), 500

@vc_bp.route('/api/vc/startups', methods=['POST'])
def create_startup():
    """
    Create a new startup.
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400
        
        # Check if portfolio exists if provided
        if data.get('portfolio_id'):
            portfolio = Portfolio.query.get(data['portfolio_id'])
            if not portfolio:
                return jsonify({'error': 'Portfolio not found'}), 404
        
        # Create new startup
        startup = Startup(
            name=data['name'],
            description=data.get('description'),
            sector=data.get('sector'),
            country=data.get('country'),
            founded_year=data.get('founded_year'),
            funding_stage=data.get('funding_stage'),
            portfolio_id=data.get('portfolio_id')
        )
        
        # Save to database
        db.session.add(startup)
        db.session.commit()
        
        return jsonify({
            'message': 'Startup created successfully',
            'startup': startup.to_dict()
        }), 201
    except Exception as e:
        logger.error(f"Error creating startup: {str(e)}")
        return jsonify({'error': str(e)}), 500

@vc_bp.route('/api/vc/startups/<int:startup_id>', methods=['GET'])
def get_startup(startup_id):
    """
    Get a specific startup.
    """
    try:
        startup = Startup.query.get(startup_id)
        if not startup:
            return jsonify({'error': 'Startup not found'}), 404
        
        return jsonify({
            'startup': startup.to_dict()
        })
    except Exception as e:
        logger.error(f"Error getting startup: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Document Upload Routes
@vc_bp.route('/api/vc/startups/<int:startup_id>/documents', methods=['POST'])
def upload_startup_document(startup_id):
    """
    Upload a document for a startup.
    """
    try:
        # Check if startup exists
        startup = Startup.query.get(startup_id)
        if not startup:
            return jsonify({'error': 'Startup not found'}), 404
        
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # Get document type
        document_type = request.form.get('document_type', 'other')
        
        # Check if file is allowed
        allowed_extensions = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt'}
        if not allowed_file(file.filename, allowed_extensions):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Secure filename and save file
        filename = secure_filename(file.filename)
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        file_path = os.path.join(upload_folder, f"startup_{startup_id}_{filename}")
        
        # Ensure upload directory exists
        os.makedirs(upload_folder, exist_ok=True)
        
        # Save file
        file.save(file_path)
        
        # Create document record
        document = StartupDocument(
            startup_id=startup_id,
            document_type=document_type,
            file_path=file_path,
            file_name=filename,
            file_size=os.path.getsize(file_path)
        )
        
        # Save to database
        db.session.add(document)
        db.session.commit()
        
        return jsonify({
            'message': 'Document uploaded successfully',
            'document': document.to_dict()
        }), 201
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        return jsonify({'error': str(e)}), 500

# LCA Data Routes
@vc_bp.route('/api/vc/startups/<int:startup_id>/lca', methods=['POST'])
def create_lca_data(startup_id):
    """
    Create LCA data for a startup.
    """
    try:
        # Check if startup exists
        startup = Startup.query.get(startup_id)
        if not startup:
            return jsonify({'error': 'Startup not found'}), 404
        
        data = request.get_json()
        
        # Create new LCA data
        lca_data = LCAData(
            startup_id=startup_id,
            product_name=data.get('product_name'),
            functional_unit=data.get('functional_unit'),
            system_boundary=data.get('system_boundary'),
            raw_materials=data.get('raw_materials'),
            manufacturing=data.get('manufacturing'),
            distribution=data.get('distribution'),
            use_phase=data.get('use_phase'),
            end_of_life=data.get('end_of_life'),
            global_warming_potential=data.get('global_warming_potential'),
            water_consumption=data.get('water_consumption'),
            energy_consumption=data.get('energy_consumption'),
            resource_depletion=data.get('resource_depletion'),
            eutrophication=data.get('eutrophication'),
            recyclability=data.get('recyclability'),
            reusability=data.get('reusability'),
            biodegradability=data.get('biodegradability')
        )
        
        # Save to database
        db.session.add(lca_data)
        db.session.commit()
        
        # Update startup with LCA data
        startup.lca_data = lca_data.to_dict()
        startup.carbon_intensity_per_unit = data.get('carbon_intensity_per_unit')
        startup.water_intensity_per_unit = data.get('water_intensity_per_unit')
        startup.energy_intensity_per_unit = data.get('energy_intensity_per_unit')
        startup.circularity_index = data.get('circularity_index')
        
        db.session.commit()
        
        return jsonify({
            'message': 'LCA data created successfully',
            'lca_data': lca_data.to_dict()
        }), 201
    except Exception as e:
        logger.error(f"Error creating LCA data: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Assessment Routes
@vc_bp.route('/api/vc/startups/<int:startup_id>/assess', methods=['POST'])
def assess_startup(startup_id):
    """
    Assess a startup against a VC firm's investment thesis.
    """
    try:
        # Check if startup exists
        startup = Startup.query.get(startup_id)
        if not startup:
            return jsonify({'error': 'Startup not found'}), 404
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('vc_firm_id'):
            return jsonify({'error': 'VC firm ID is required'}), 400
        
        # Check if VC firm exists
        vc_firm = VCFirm.query.get(data['vc_firm_id'])
        if not vc_firm:
            return jsonify({'error': 'VC firm not found'}), 404
        
        # Check if investment thesis exists if provided
        investment_thesis_id = data.get('investment_thesis_id')
        if investment_thesis_id:
            thesis = InvestmentThesis.query.get(investment_thesis_id)
            if not thesis:
                return jsonify({'error': 'Investment thesis not found'}), 404
        
        # For now, we'll use dummy assessment logic
        # In a real implementation, this would use AI/ML models to assess the startup
        
        # Create assessment
        assessment = StartupAssessment(
            startup_id=startup_id,
            vc_firm_id=data['vc_firm_id'],
            investment_thesis_id=investment_thesis_id,
            product_viability_score=data.get('product_viability_score', 0.75),
            operational_maturity_score=data.get('operational_maturity_score', 0.65),
            governance_risk_score=data.get('governance_risk_score', 0.8),
            strategic_fit_score=data.get('strategic_fit_score', 0.7),
            market_signal_score=data.get('market_signal_score', 0.6),
            overall_readiness_score=data.get('overall_readiness_score', 0.7),
            product_viability_details=data.get('product_viability_details', {}),
            operational_maturity_details=data.get('operational_maturity_details', {}),
            governance_risk_details=data.get('governance_risk_details', {}),
            strategic_fit_details=data.get('strategic_fit_details', {}),
            market_signal_details=data.get('market_signal_details', {}),
            ai_insights=data.get('ai_insights', 'This startup shows promising alignment with your investment thesis.'),
            improvement_recommendations=data.get('improvement_recommendations', {})
        )
        
        # Save to database
        db.session.add(assessment)
        db.session.commit()
        
        return jsonify({
            'message': 'Startup assessed successfully',
            'assessment': assessment.to_dict()
        }), 201
    except Exception as e:
        logger.error(f"Error assessing startup: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Materiality Matrix Routes
@vc_bp.route('/api/vc/startups/<int:startup_id>/materiality', methods=['POST'])
def create_materiality_matrix(startup_id):
    """
    Create a materiality matrix for a startup.
    """
    try:
        # Check if startup exists
        startup = Startup.query.get(startup_id)
        if not startup:
            return jsonify({'error': 'Startup not found'}), 404
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('matrix_data'):
            return jsonify({'error': 'Matrix data is required'}), 400
        
        # Create new materiality matrix
        matrix = MaterialityMatrix(
            startup_id=startup_id,
            matrix_data=data['matrix_data'],
            sector=data.get('sector'),
            geography=data.get('geography'),
            company_size=data.get('company_size'),
            regulatory_exposure=data.get('regulatory_exposure')
        )
        
        # Save to database
        db.session.add(matrix)
        db.session.commit()
        
        # Update startup with materiality matrix
        startup.materiality_matrix = matrix.to_dict()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Materiality matrix created successfully',
            'materiality_matrix': matrix.to_dict()
        }), 201
    except Exception as e:
        logger.error(f"Error creating materiality matrix: {str(e)}")
        return jsonify({'error': str(e)}), 500

# UI Routes
@vc_bp.route('/vc-lens', methods=['GET'])
def vc_lens():
    """
    Render the VC Lens page.
    """
    return render_template('vc_lens.html', active_page='vc-lens')

@vc_bp.route('/vc-lens/startup/<int:startup_id>', methods=['GET'])
def startup_detail(startup_id):
    """
    Render the startup detail page.
    """
    startup = Startup.query.get(startup_id)
    if not startup:
        return render_template('404.html'), 404
    
    return render_template('startup_detail.html', startup=startup, active_page='vc-lens')

@vc_bp.route('/vc-lens/assessment/<int:startup_id>/<int:vc_firm_id>', methods=['GET'])
def startup_assessment(startup_id, vc_firm_id):
    """
    Render the startup assessment page.
    """
    startup = Startup.query.get(startup_id)
    vc_firm = VCFirm.query.get(vc_firm_id)
    
    if not startup or not vc_firm:
        return render_template('404.html'), 404
    
    # Get assessment if it exists
    assessment = StartupAssessment.query.filter_by(
        startup_id=startup_id, 
        vc_firm_id=vc_firm_id
    ).first()
    
    return render_template(
        'startup_assessment.html', 
        startup=startup, 
        vc_firm=vc_firm, 
        assessment=assessment,
        active_page='vc-lens'
    ) 