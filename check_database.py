"""
Enhanced Database Inspector
Comprehensive tool for checking database contents, integrity, and statistics
"""
from app import create_app
from models import (
    db, User, Poem, Comment, Like, SavedPoem, Follow, 
    Notification, Highlight, HighlightPoem, UserActivity, Visitor
)
from datetime import datetime, timedelta
from collections import defaultdict


class DatabaseInspector:
    """Comprehensive database inspection and reporting"""
    
    def __init__(self):
        self.app = create_app()
    
    def _print_section(self, title):
        """Print a formatted section header"""
        print("\n" + "="*70)
        print(f"  {title}")
        print("="*70)
    
    def _print_subsection(self, title):
        """Print a formatted subsection header"""
        print(f"\n{title}")
        print("-"*70)
    
    def check_basic_stats(self):
        """Display basic database statistics"""
        with self.app.app_context():
            self._print_section("📊 DATABASE OVERVIEW")
            
            stats = {
                'Users': User.query.count(),
                'Poems': Poem.query.count(),
                'Comments': Comment.query.count(),
                'Likes': Like.query.count(),
                'Saved Poems': SavedPoem.query.count(),
                'Follows': Follow.query.count(),
                'Notifications': Notification.query.count(),
                'Highlights': Highlight.query.count(),
                'User Activities': UserActivity.query.count(),
                'Visitors': Visitor.query.count()
            }
            
            for key, value in stats.items():
                print(f"  {key:.<30} {value:>6}")
    
    def check_users(self, detailed=False):
        """Display user information"""
        with self.app.app_context():
            self._print_section("👥 USERS")
            
            users = User.query.order_by(User.created_at.desc()).all()
            
            # Categorize users
            admins = [u for u in users if u.is_admin]
            classic_poets = [u for u in users if '@poetryvault.com' in u.email or '@poetry.vault' in u.email]
            real_users = [u for u in users if u not in admins + classic_poets]
            
            print(f"\n  Total Users: {len(users)}")
            print(f"  Admins: {len(admins)}")
            print(f"  Classic Poets: {len(classic_poets)}")
            print(f"  Real Users: {len(real_users)}")
            
            if admins:
                self._print_subsection("🔑 Admin Users")
                for user in admins:
                    poems_count = Poem.query.filter_by(user_id=user.id).count()
                    print(f"  • {user.username:.<30} {user.email:.<40} {poems_count} poems")
            
            if real_users:
                self._print_subsection("👤 Real Users")
                for user in real_users:
                    poems_count = Poem.query.filter_by(user_id=user.id).count()
                    followers = Follow.query.filter_by(followed_id=user.id).count()
                    following = Follow.query.filter_by(follower_id=user.id).count()
                    created = user.created_at.strftime('%Y-%m-%d') if user.created_at else 'Unknown'
                    print(f"  • {user.username:.<20} {poems_count:>3} poems | {followers:>3} followers | {following:>3} following | {created}")
            
            if detailed and classic_poets:
                self._print_subsection("🎭 Classic Poets")
                for user in classic_poets:
                    poems_count = Poem.query.filter_by(user_id=user.id).count()
                    print(f"  • {user.username:.<30} {poems_count:>3} poems")
    
    def check_poems(self, limit=10):
        """Display poem statistics"""
        with self.app.app_context():
            self._print_section("📚 POEMS")
            
            total_poems = Poem.query.count()
            classic_poems = Poem.query.filter_by(is_classic=True).count()
            user_poems = Poem.query.filter_by(is_classic=False).count()
            anonymous_poems = Poem.query.filter_by(is_anonymous=True).count()
            
            print(f"\n  Total Poems: {total_poems}")
            print(f"  Classic Poems: {classic_poems}")
            print(f"  User Poems: {user_poems}")
            print(f"  Anonymous Poems: {anonymous_poems}")
            
            # Category breakdown
            self._print_subsection("📂 Poems by Category")
            categories = db.session.query(
                Poem.category, 
                db.func.count(Poem.id)
            ).group_by(Poem.category).order_by(db.func.count(Poem.id).desc()).all()
            
            for category, count in categories[:15]:  # Top 15 categories
                if category:
                    print(f"  {category:.<30} {count:>4} poems")
            
            # Most liked poems
            self._print_subsection(f"❤️  Most Liked Poems (Top {limit})")
            poems_with_likes = db.session.query(
                Poem, db.func.count(Like.id).label('like_count')
            ).outerjoin(Like).group_by(Poem.id).order_by(db.text('like_count DESC')).limit(limit).all()
            
            for poem, like_count in poems_with_likes:
                if like_count > 0:
                    print(f"  {poem.title[:40]:.<42} {like_count:>3} likes | by {poem.author.username}")
            
            # Most commented poems
            self._print_subsection(f"💬 Most Commented Poems (Top {limit})")
            poems_with_comments = db.session.query(
                Poem, db.func.count(Comment.id).label('comment_count')
            ).outerjoin(Comment).group_by(Poem.id).order_by(db.text('comment_count DESC')).limit(limit).all()
            
            for poem, comment_count in poems_with_comments:
                if comment_count > 0:
                    print(f"  {poem.title[:40]:.<42} {comment_count:>3} comments | by {poem.author.username}")
    
    def check_engagement(self):
        """Display engagement statistics"""
        with self.app.app_context():
            self._print_section("📈 ENGAGEMENT METRICS")
            
            # Comments
            total_comments = Comment.query.count()
            users_who_commented = db.session.query(Comment.user_id).distinct().count()
            
            print(f"\n  Total Comments: {total_comments}")
            print(f"  Users Who Commented: {users_who_commented}")
            
            # Likes
            total_likes = Like.query.count()
            users_who_liked = db.session.query(Like.user_id).distinct().count()
            
            print(f"\n  Total Likes: {total_likes}")
            print(f"  Users Who Liked: {users_who_liked}")
            
            # Follows
            total_follows = Follow.query.count()
            
            print(f"\n  Total Follows: {total_follows}")
            
            # Saved poems
            total_saved = SavedPoem.query.count()
            users_who_saved = db.session.query(SavedPoem.user_id).distinct().count()
            
            print(f"\n  Total Saved Poems: {total_saved}")
            print(f"  Users Who Saved: {users_who_saved}")
            
            # Most active users
            self._print_subsection("🌟 Most Active Users")
            active_users = db.session.query(
                User,
                db.func.count(Comment.id).label('comment_count')
            ).outerjoin(Comment).group_by(User.id).order_by(db.text('comment_count DESC')).limit(10).all()
            
            for user, comment_count in active_users:
                if comment_count > 0:
                    poems_count = Poem.query.filter_by(user_id=user.id, is_classic=False).count()
                    likes_given = Like.query.filter_by(user_id=user.id).count()
                    print(f"  {user.username:.<25} {poems_count:>3} poems | {comment_count:>3} comments | {likes_given:>3} likes")
    
    def check_analytics(self):
        """Display analytics data"""
        with self.app.app_context():
            self._print_section("📊 ANALYTICS")
            
            total_visitors = Visitor.query.count()
            instagram_visitors = Visitor.query.filter_by(source='instagram').count()
            
            print(f"\n  Total Visitors: {total_visitors}")
            print(f"  Instagram Visitors: {instagram_visitors}")
            
            # Recent visitors
            self._print_subsection("👁️  Recent Visitors (Last 20)")
            recent_visitors = Visitor.query.order_by(Visitor.last_visit.desc()).limit(20).all()
            
            for visitor in recent_visitors:
                nickname = visitor.nickname or 'Anonymous'
                last_visit = visitor.last_visit.strftime('%Y-%m-%d %H:%M') if visitor.last_visit else 'Unknown'
                print(f"  {nickname:.<20} {visitor.source:.<15} {visitor.visit_count:>3} visits | Last: {last_visit}")
            
            # Activity breakdown
            self._print_subsection("📈 Activity Breakdown")
            activities = db.session.query(
                UserActivity.activity_type,
                db.func.count(UserActivity.id)
            ).group_by(UserActivity.activity_type).order_by(db.func.count(UserActivity.id).desc()).all()
            
            for activity_type, count in activities:
                print(f"  {activity_type:.<30} {count:>5}")
    
    def check_integrity(self):
        """Check database integrity"""
        with self.app.app_context():
            self._print_section("🔍 DATABASE INTEGRITY CHECK")
            
            issues = []
            
            # Check for orphaned poems
            orphaned_poems = Poem.query.filter(~Poem.user_id.in_(
                db.session.query(User.id)
            )).count()
            if orphaned_poems > 0:
                issues.append(f"⚠️  {orphaned_poems} poems without valid user")
            
            # Check for orphaned comments
            orphaned_comments = Comment.query.filter(~Comment.user_id.in_(
                db.session.query(User.id)
            )).count()
            if orphaned_comments > 0:
                issues.append(f"⚠️  {orphaned_comments} comments without valid user")
            
            # Check for orphaned likes
            orphaned_likes = Like.query.filter(~Like.user_id.in_(
                db.session.query(User.id)
            )).count()
            if orphaned_likes > 0:
                issues.append(f"⚠️  {orphaned_likes} likes without valid user")
            
            if issues:
                print("\n  Issues Found:")
                for issue in issues:
                    print(f"  {issue}")
            else:
                print("\n  ✅ No integrity issues found")
    
    def run_full_check(self):
        """Run all checks"""
        print("\n" + "="*70)
        print("  🔍 COMPREHENSIVE DATABASE INSPECTION")
        print("="*70)
        print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.check_basic_stats()
        self.check_users(detailed=False)
        self.check_poems(limit=5)
        self.check_engagement()
        self.check_analytics()
        self.check_integrity()
        
        print("\n" + "="*70)
        print("  ✅ INSPECTION COMPLETE")
        print("="*70 + "\n")


def main():
    """Main entry point"""
    import sys
    
    inspector = DatabaseInspector()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'stats':
            inspector.check_basic_stats()
        elif command == 'users':
            inspector.check_users(detailed=True)
        elif command == 'poems':
            inspector.check_poems(limit=20)
        elif command == 'engagement':
            inspector.check_engagement()
        elif command == 'analytics':
            inspector.check_analytics()
        elif command == 'integrity':
            inspector.check_integrity()
        elif command == 'full':
            inspector.run_full_check()
        else:
            print("Enhanced Database Inspector")
            print("="*70)
            print("\nUsage:")
            print("  python check_database.py [command]")
            print("\nCommands:")
            print("  stats       - Basic statistics")
            print("  users       - User information")
            print("  poems       - Poem statistics")
            print("  engagement  - Engagement metrics")
            print("  analytics   - Analytics data")
            print("  integrity   - Database integrity check")
            print("  full        - Run all checks (default)")
            print("\nExamples:")
            print("  python check_database.py")
            print("  python check_database.py users")
            print("  python check_database.py full")
    else:
        # Default: run full check
        inspector.run_full_check()


if __name__ == '__main__':
    main()
