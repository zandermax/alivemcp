"""
Application-level helpers for Live (build, variant, dialogs, version).
"""


class AppInfoMixin:
    def get_build_id(self):
        """Get Ableton Live build identifier (Live 12+)

        See Also:
            Wiki: docs/wiki/tools/get_build_id.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            import Live

            app = Live.Application.get_application()

            if hasattr(app, "get_build_id"):
                return {"ok": True, "build_id": str(app.get_build_id())}
            else:
                return {"ok": False, "error": "get_build_id not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_variant(self):
        """Get Ableton Live variant (Suite, Standard, Intro) (Live 12+)

        See Also:
            Wiki: docs/wiki/tools/get_variant.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            import Live

            app = Live.Application.get_application()

            if hasattr(app, "get_variant"):
                return {"ok": True, "variant": str(app.get_variant())}
            else:
                return {"ok": False, "error": "get_variant not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def show_message_box(self, message, title="Message"):
        """Show message box dialog to user (Live 12+)

        See Also:
            Wiki: docs/wiki/tools/show_message_box.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            import Live

            app = Live.Application.get_application()

            if hasattr(app, "show_message"):
                result = app.show_message(str(message))
                return {
                    "ok": True,
                    "message": "Message shown",
                    "button_pressed": int(result) if result is not None else 0,
                }
            else:
                return {"ok": False, "error": "show_message not available (Live 12+ only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_application_version(self):
        """Get full Ableton Live version information

        See Also:
            Wiki: docs/wiki/tools/get_application_version.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            import Live

            app = Live.Application.get_application()

            version_info = {
                "ok": True,
                "major_version": int(app.get_major_version()),
                "minor_version": int(app.get_minor_version()),
                "bugfix_version": int(app.get_bugfix_version()),
            }

            if hasattr(app, "get_build_id"):
                version_info["build_id"] = str(app.get_build_id())

            if hasattr(app, "get_variant"):
                version_info["variant"] = str(app.get_variant())

            return version_info
        except Exception as e:
            return {"ok": False, "error": str(e)}
