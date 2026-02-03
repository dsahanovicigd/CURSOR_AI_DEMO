from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.admin import admin_bp
from app.models.ticket import Ticket
from app.models.user import User
from app.models.ticket_status_history import TicketStatusHistory
from sqlalchemy import func, extract
from datetime import datetime, timedelta

def require_admin():
    """Decorator to require admin access"""
    def decorator(f):
        @jwt_required()
        def wrapper(*args, **kwargs):
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if not current_user.is_admin_user():
                return jsonify({
                    'status': 'error',
                    'message': 'Access denied',
                    'code': 'FORBIDDEN'
                }), 403
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    """
    Get admin dashboard metrics
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    responses:
      200:
        description: Dashboard metrics
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user.is_admin_user():
        return jsonify({
            'status': 'error',
            'message': 'Access denied',
            'code': 'FORBIDDEN'
        }), 403
    
    # Total tickets by status
    total_tickets = Ticket.query.count()
    open_tickets = Ticket.query.filter_by(status=Ticket.STATUS_OPEN).count()
    in_progress_tickets = Ticket.query.filter_by(status=Ticket.STATUS_IN_PROGRESS).count()
    resolved_tickets = Ticket.query.filter_by(status=Ticket.STATUS_RESOLVED).count()
    closed_tickets = Ticket.query.filter_by(status=Ticket.STATUS_CLOSED).count()
    
    # Tickets by priority
    urgent_tickets = Ticket.query.filter_by(priority=Ticket.PRIORITY_URGENT).count()
    high_tickets = Ticket.query.filter_by(priority=Ticket.PRIORITY_HIGH).count()
    medium_tickets = Ticket.query.filter_by(priority=Ticket.PRIORITY_MEDIUM).count()
    low_tickets = Ticket.query.filter_by(priority=Ticket.PRIORITY_LOW).count()
    
    # Tickets by category
    technical_tickets = Ticket.query.filter_by(category=Ticket.CATEGORY_TECHNICAL).count()
    billing_tickets = Ticket.query.filter_by(category=Ticket.CATEGORY_BILLING).count()
    general_tickets = Ticket.query.filter_by(category=Ticket.CATEGORY_GENERAL).count()
    feature_tickets = Ticket.query.filter_by(category=Ticket.CATEGORY_FEATURE_REQUEST).count()
    
    # Average resolution time
    resolved_tickets_with_time = Ticket.query.filter(
        Ticket.status.in_([Ticket.STATUS_RESOLVED, Ticket.STATUS_CLOSED]),
        Ticket.resolved_at.isnot(None)
    ).all()
    
    avg_resolution_time = None
    if resolved_tickets_with_time:
        total_seconds = sum(
            (t.resolved_at - t.created_at).total_seconds() 
            for t in resolved_tickets_with_time
        )
        avg_seconds = total_seconds / len(resolved_tickets_with_time)
        avg_resolution_time = {
            'hours': round(avg_seconds / 3600, 2),
            'days': round(avg_seconds / 86400, 2)
        }
    
    # SLA compliance
    sla_breached = Ticket.query.filter(
        Ticket.sla_resolution_deadline.isnot(None),
        Ticket.sla_resolution_deadline < datetime.utcnow(),
        ~Ticket.status.in_([Ticket.STATUS_RESOLVED, Ticket.STATUS_CLOSED])
    ).count()
    
    sla_compliance_rate = None
    if total_tickets > 0:
        sla_compliant = total_tickets - sla_breached
        sla_compliance_rate = round((sla_compliant / total_tickets) * 100, 2)
    
    # Agent performance
    agents = User.query.filter_by(role=User.ROLE_AGENT, is_active=True).all()
    agent_performance = []
    for agent in agents:
        assigned_tickets = Ticket.query.filter_by(assigned_to_id=agent.id).count()
        resolved_tickets_count = Ticket.query.filter_by(
            assigned_to_id=agent.id,
            status__in=[Ticket.STATUS_RESOLVED, Ticket.STATUS_CLOSED]
        ).count()
        open_tickets_count = agent.get_open_ticket_count()
        
        agent_performance.append({
            'agent_id': agent.id,
            'agent_name': agent.full_name,
            'assigned_tickets': assigned_tickets,
            'resolved_tickets': resolved_tickets_count,
            'open_tickets': open_tickets_count,
            'resolution_rate': round((resolved_tickets_count / assigned_tickets * 100) if assigned_tickets > 0 else 0, 2)
        })
    
    return jsonify({
        'tickets': {
            'total': total_tickets,
            'open': open_tickets,
            'in_progress': in_progress_tickets,
            'resolved': resolved_tickets,
            'closed': closed_tickets
        },
        'by_priority': {
            'urgent': urgent_tickets,
            'high': high_tickets,
            'medium': medium_tickets,
            'low': low_tickets
        },
        'by_category': {
            'technical': technical_tickets,
            'billing': billing_tickets,
            'general': general_tickets,
            'feature_request': feature_tickets
        },
        'average_resolution_time': avg_resolution_time,
        'sla_compliance': {
            'breached': sla_breached,
            'compliance_rate': sla_compliance_rate
        },
        'agent_performance': agent_performance
    }), 200

@admin_bp.route('/reports/tickets', methods=['GET'])
@jwt_required()
def get_ticket_report():
    """
    Get ticket volume report
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    parameters:
      - in: query
        name: period
        type: string
        enum: [daily, weekly, monthly]
        default: daily
      - in: query
        name: start_date
        type: string
        format: date
      - in: query
        name: end_date
        type: string
        format: date
    responses:
      200:
        description: Ticket volume report
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user.is_admin_user():
        return jsonify({
            'status': 'error',
            'message': 'Access denied',
            'code': 'FORBIDDEN'
        }), 403
    
    period = request.args.get('period', 'daily')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Build date range
    if start_date and end_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
        except ValueError:
            return jsonify({
                'status': 'error',
                'message': 'Invalid date format. Use YYYY-MM-DD',
                'code': 'VALIDATION_ERROR'
            }), 400
    else:
        # Default to last 30 days
        end = datetime.utcnow()
        start = end - timedelta(days=30)
    
    query = Ticket.query.filter(
        Ticket.created_at >= start,
        Ticket.created_at < end
    )
    
    # Group by period
    if period == 'daily':
        tickets_by_period = db.session.query(
            func.date(Ticket.created_at).label('date'),
            func.count(Ticket.id).label('count')
        ).filter(
            Ticket.created_at >= start,
            Ticket.created_at < end
        ).group_by(func.date(Ticket.created_at)).all()
    elif period == 'weekly':
        tickets_by_period = db.session.query(
            func.strftime('%Y-W%W', Ticket.created_at).label('week'),
            func.count(Ticket.id).label('count')
        ).filter(
            Ticket.created_at >= start,
            Ticket.created_at < end
        ).group_by(func.strftime('%Y-W%W', Ticket.created_at)).all()
    else:  # monthly
        tickets_by_period = db.session.query(
            func.strftime('%Y-%m', Ticket.created_at).label('month'),
            func.count(Ticket.id).label('count')
        ).filter(
            Ticket.created_at >= start,
            Ticket.created_at < end
        ).group_by(func.strftime('%Y-%m', Ticket.created_at)).all()
    
    total_tickets = query.count()
    tickets_by_status = {}
    tickets_by_priority = {}
    tickets_by_category = {}
    
    for status in [Ticket.STATUS_OPEN, Ticket.STATUS_ASSIGNED, Ticket.STATUS_IN_PROGRESS, 
                    Ticket.STATUS_RESOLVED, Ticket.STATUS_CLOSED]:
        tickets_by_status[status] = query.filter_by(status=status).count()
    
    for priority in [Ticket.PRIORITY_LOW, Ticket.PRIORITY_MEDIUM, Ticket.PRIORITY_HIGH, Ticket.PRIORITY_URGENT]:
        tickets_by_priority[priority] = query.filter_by(priority=priority).count()
    
    for category in [Ticket.CATEGORY_TECHNICAL, Ticket.CATEGORY_BILLING, 
                     Ticket.CATEGORY_GENERAL, Ticket.CATEGORY_FEATURE_REQUEST]:
        tickets_by_category[category] = query.filter_by(category=category).count()
    
    return jsonify({
        'period': period,
        'start_date': start_date or start.strftime('%Y-%m-%d'),
        'end_date': end_date or (end - timedelta(days=1)).strftime('%Y-%m-%d'),
        'total_tickets': total_tickets,
        'tickets_by_period': [{'period': str(p[0]), 'count': p[1]} for p in tickets_by_period],
        'tickets_by_status': tickets_by_status,
        'tickets_by_priority': tickets_by_priority,
        'tickets_by_category': tickets_by_category
    }), 200

@admin_bp.route('/reports/agents', methods=['GET'])
@jwt_required()
def get_agent_report():
    """
    Get agent performance report
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    parameters:
      - in: query
        name: agent_id
        type: integer
      - in: query
        name: start_date
        type: string
        format: date
      - in: query
        name: end_date
        type: string
        format: date
    responses:
      200:
        description: Agent performance report
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user.is_admin_user():
        return jsonify({
            'status': 'error',
            'message': 'Access denied',
            'code': 'FORBIDDEN'
        }), 403
    
    agent_id = request.args.get('agent_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Build date range
    if start_date and end_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
        except ValueError:
            return jsonify({
                'status': 'error',
                'message': 'Invalid date format',
                'code': 'VALIDATION_ERROR'
            }), 400
    else:
        end = datetime.utcnow()
        start = end - timedelta(days=30)
    
    query = User.query.filter_by(role=User.ROLE_AGENT, is_active=True)
    if agent_id:
        query = query.filter_by(id=agent_id)
    
    agents = query.all()
    agent_reports = []
    
    for agent in agents:
        # Tickets assigned in period
        assigned_tickets = Ticket.query.filter(
            Ticket.assigned_to_id == agent.id,
            Ticket.created_at >= start,
            Ticket.created_at < end
        ).count()
        
        # Resolved tickets
        resolved_tickets = Ticket.query.filter(
            Ticket.assigned_to_id == agent.id,
            Ticket.status.in_([Ticket.STATUS_RESOLVED, Ticket.STATUS_CLOSED]),
            Ticket.resolved_at.isnot(None),
            Ticket.resolved_at >= start,
            Ticket.resolved_at < end
        ).all()
        
        # Calculate average resolution time
        avg_resolution_time = None
        if resolved_tickets:
            total_seconds = sum(
                (t.resolved_at - t.created_at).total_seconds()
                for t in resolved_tickets
            )
            avg_seconds = total_seconds / len(resolved_tickets)
            avg_resolution_time = {
                'hours': round(avg_seconds / 3600, 2),
                'days': round(avg_seconds / 86400, 2)
            }
        
        # SLA compliance
        sla_breached = Ticket.query.filter(
            Ticket.assigned_to_id == agent.id,
            Ticket.sla_resolution_deadline.isnot(None),
            Ticket.sla_resolution_deadline < datetime.utcnow(),
            ~Ticket.status.in_([Ticket.STATUS_RESOLVED, Ticket.STATUS_CLOSED])
        ).count()
        
        agent_reports.append({
            'agent_id': agent.id,
            'agent_name': agent.full_name,
            'email': agent.email,
            'assigned_tickets': assigned_tickets,
            'resolved_tickets': len(resolved_tickets),
            'open_tickets': agent.get_open_ticket_count(),
            'average_resolution_time': avg_resolution_time,
            'sla_breached': sla_breached,
            'resolution_rate': round((len(resolved_tickets) / assigned_tickets * 100) if assigned_tickets > 0 else 0, 2)
        })
    
    return jsonify({
        'period': {
            'start_date': start_date or start.strftime('%Y-%m-%d'),
            'end_date': end_date or (end - timedelta(days=1)).strftime('%Y-%m-%d')
        },
        'agents': agent_reports
    }), 200

@admin_bp.route('/reports/sla', methods=['GET'])
@jwt_required()
def get_sla_report():
    """
    Get SLA compliance report
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    responses:
      200:
        description: SLA compliance report
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user.is_admin_user():
        return jsonify({
            'status': 'error',
            'message': 'Access denied',
            'code': 'FORBIDDEN'
        }), 403
    
    # Total tickets with SLA
    total_with_sla = Ticket.query.filter(
        Ticket.sla_resolution_deadline.isnot(None)
    ).count()
    
    # Breached tickets
    breached_tickets = Ticket.query.filter(
        Ticket.sla_resolution_deadline.isnot(None),
        Ticket.sla_resolution_deadline < datetime.utcnow(),
        ~Ticket.status.in_([Ticket.STATUS_RESOLVED, Ticket.STATUS_CLOSED])
    ).all()
    
    # Breached by priority
    breached_by_priority = {}
    for priority in [Ticket.PRIORITY_LOW, Ticket.PRIORITY_MEDIUM, Ticket.PRIORITY_HIGH, Ticket.PRIORITY_URGENT]:
        breached_by_priority[priority] = len([
            t for t in breached_tickets if t.priority == priority
        ])
    
    # Compliance rate
    compliance_rate = None
    if total_with_sla > 0:
        compliant = total_with_sla - len(breached_tickets)
        compliance_rate = round((compliant / total_with_sla) * 100, 2)
    
    return jsonify({
        'total_tickets_with_sla': total_with_sla,
        'breached_tickets': len(breached_tickets),
        'compliant_tickets': total_with_sla - len(breached_tickets),
        'compliance_rate': compliance_rate,
        'breached_by_priority': breached_by_priority,
        'breached_tickets_detail': [{
            'ticket_id': t.id,
            'ticket_number': t.ticket_number,
            'priority': t.priority,
            'sla_deadline': t.sla_resolution_deadline.isoformat() if t.sla_resolution_deadline else None,
            'hours_overdue': round((datetime.utcnow() - t.sla_resolution_deadline).total_seconds() / 3600, 2) if t.sla_resolution_deadline else None
        } for t in breached_tickets[:50]]  # Limit to 50 most recent
    }), 200
