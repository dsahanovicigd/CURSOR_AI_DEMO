"""Email notification service for ticket system"""
from flask import current_app
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EmailService:
    """Service for sending email notifications"""
    
    @staticmethod
    def send_ticket_created_notification(ticket):
        """Send email notification when ticket is created (FR-003, FR-035)"""
        try:
            subject = f"Ticket Created: {ticket.ticket_number}"
            body = f"""
Hello,

Your support ticket has been created successfully.

Ticket Number: {ticket.ticket_number}
Subject: {ticket.subject}
Priority: {ticket.priority.title()}
Category: {ticket.category.replace('_', ' ').title()}
Status: {ticket.status.title()}

You can track your ticket status using the ticket number above.

Best regards,
Support Team
"""
            EmailService._send_email(ticket.customer_email, subject, body)
            logger.info(f"Ticket creation email sent to {ticket.customer_email} for ticket {ticket.ticket_number}")
        except Exception as e:
            logger.error(f"Failed to send ticket creation email: {str(e)}")
    
    @staticmethod
    def send_ticket_assigned_notification(ticket, agent):
        """Send email notification when ticket is assigned (FR-007, FR-035)"""
        try:
            subject = f"New Ticket Assigned: {ticket.ticket_number}"
            body = f"""
Hello {agent.full_name},

A new ticket has been assigned to you.

Ticket Number: {ticket.ticket_number}
Subject: {ticket.subject}
Priority: {ticket.priority.title()}
Category: {ticket.category.replace('_', ' ').title()}
Customer: {ticket.customer_email}

Please review and respond promptly.

Best regards,
Support Team
"""
            EmailService._send_email(agent.email, subject, body)
            logger.info(f"Ticket assignment email sent to {agent.email} for ticket {ticket.ticket_number}")
        except Exception as e:
            logger.error(f"Failed to send ticket assignment email: {str(e)}")
    
    @staticmethod
    def send_status_change_notification(ticket, old_status, changed_by=None):
        """Send email notification when ticket status changes (FR-014, FR-035)"""
        try:
            # Notify customer
            subject = f"Ticket Status Updated: {ticket.ticket_number}"
            body = f"""
Hello,

Your ticket status has been updated.

Ticket Number: {ticket.ticket_number}
Subject: {ticket.subject}
Previous Status: {old_status.title()}
New Status: {ticket.status.title()}

You can track your ticket status using the ticket number above.

Best regards,
Support Team
"""
            EmailService._send_email(ticket.customer_email, subject, body)
            
            # Notify assigned agent if different from changer
            if ticket.assigned_to and changed_by and ticket.assigned_to.id != changed_by.id:
                agent_subject = f"Ticket Status Updated: {ticket.ticket_number}"
                agent_body = f"""
Hello {ticket.assigned_to.full_name},

Ticket {ticket.ticket_number} status has been updated to {ticket.status.title()}.

Subject: {ticket.subject}
Changed by: {changed_by.full_name}

Best regards,
Support Team
"""
                EmailService._send_email(ticket.assigned_to.email, agent_subject, agent_body)
            
            logger.info(f"Status change email sent for ticket {ticket.ticket_number}")
        except Exception as e:
            logger.error(f"Failed to send status change email: {str(e)}")
    
    @staticmethod
    def send_comment_notification(ticket, comment, commenter_name):
        """Send email notification when comment is added (FR-018, FR-035)"""
        try:
            # Notify customer if comment is public
            if not comment.is_internal:
                subject = f"New Comment on Ticket: {ticket.ticket_number}"
                body = f"""
Hello,

A new comment has been added to your ticket.

Ticket Number: {ticket.ticket_number}
Subject: {ticket.subject}
Comment by: {commenter_name}

{comment.content[:200]}{'...' if len(comment.content) > 200 else ''}

You can view the full comment and respond using the ticket number above.

Best regards,
Support Team
"""
                EmailService._send_email(ticket.customer_email, subject, body)
            
            # Notify assigned agent if comment is from customer
            if ticket.assigned_to and comment.is_internal == False:
                agent_subject = f"New Customer Comment: {ticket.ticket_number}"
                agent_body = f"""
Hello {ticket.assigned_to.full_name},

A new comment has been added to ticket {ticket.ticket_number}.

Subject: {ticket.subject}
Comment by: {commenter_name}

{comment.content[:200]}{'...' if len(comment.content) > 200 else ''}

Please review and respond if needed.

Best regards,
Support Team
"""
                EmailService._send_email(ticket.assigned_to.email, agent_subject, agent_body)
            
            logger.info(f"Comment notification email sent for ticket {ticket.ticket_number}")
        except Exception as e:
            logger.error(f"Failed to send comment notification email: {str(e)}")
    
    @staticmethod
    def send_sla_warning_notification(ticket, deadline_type='response'):
        """Send email notification when SLA deadline is approaching (FR-035)"""
        try:
            deadline = ticket.sla_response_deadline if deadline_type == 'response' else ticket.sla_resolution_deadline
            hours_remaining = (deadline - datetime.utcnow()).total_seconds() / 3600
            
            subject = f"SLA Deadline Approaching: {ticket.ticket_number}"
            body = f"""
Hello,

This is a reminder that the SLA deadline for the following ticket is approaching.

Ticket Number: {ticket.ticket_number}
Subject: {ticket.subject}
Priority: {ticket.priority.title()}
Deadline Type: {deadline_type.title()}
Hours Remaining: {hours_remaining:.1f}

Please take action to meet the SLA deadline.

Best regards,
Support Team
"""
            # Notify agent
            if ticket.assigned_to:
                EmailService._send_email(ticket.assigned_to.email, subject, body)
            
            # Notify admin
            from app.models.user import User
            admins = User.query.filter_by(role=User.ROLE_ADMIN, is_active=True).all()
            for admin in admins:
                EmailService._send_email(admin.email, subject, body)
            
            logger.info(f"SLA warning email sent for ticket {ticket.ticket_number}")
        except Exception as e:
            logger.error(f"Failed to send SLA warning email: {str(e)}")
    
    @staticmethod
    def send_sla_breached_notification(ticket):
        """Send email notification when SLA is breached (FR-022, FR-035)"""
        try:
            subject = f"SLA BREACHED: {ticket.ticket_number}"
            body = f"""
URGENT: SLA Breach Alert

Ticket Number: {ticket.ticket_number}
Subject: {ticket.subject}
Priority: {ticket.priority.title()}
Status: {ticket.status.title()}

The SLA deadline for this ticket has been breached. Immediate action is required.

Best regards,
Support Team
"""
            # Notify agent
            if ticket.assigned_to:
                EmailService._send_email(ticket.assigned_to.email, subject, body)
            
            # Notify admin
            from app.models.user import User
            admins = User.query.filter_by(role=User.ROLE_ADMIN, is_active=True).all()
            for admin in admins:
                EmailService._send_email(admin.email, subject, body)
            
            logger.warning(f"SLA breach email sent for ticket {ticket.ticket_number}")
        except Exception as e:
            logger.error(f"Failed to send SLA breach email: {str(e)}")
    
    @staticmethod
    def _send_email(to_email, subject, body):
        """Internal method to send email"""
        # In production, this would use a real email service (SendGrid, SES, etc.)
        # For now, we'll log it and optionally use Flask-Mail if configured
        logger.info(f"Email would be sent to {to_email}: {subject}")
        
        # If Flask-Mail is configured, use it
        try:
            from flask_mail import Message
            from app import mail
            
            if mail:
                msg = Message(
                    subject=subject,
                    recipients=[to_email],
                    body=body
                )
                mail.send(msg)
                logger.info(f"Email sent via Flask-Mail to {to_email}")
        except ImportError:
            # Flask-Mail not installed, just log
            logger.debug(f"Flask-Mail not available, email logged only")
        except Exception as e:
            logger.error(f"Failed to send email via Flask-Mail: {str(e)}")
