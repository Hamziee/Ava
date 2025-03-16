import json
import os
from pathlib import Path
from typing import Dict, Optional, Any, Union

class TranslationModule:
    """A convenience wrapper for accessing module translations."""
    def __init__(self, translations: Dict[str, Any], common_translations: Dict[str, Any], default_translations: Dict[str, Any], module_name: str):
        self._translations = translations
        self._common = common_translations
        self._default = default_translations
        self._module_name = module_name

    def __getattr__(self, key: str) -> Any:
        """Allow accessing translations as attributes with proper fallback chain."""
        # First try module-specific translations
        if key in self._translations:
            return self._translations[key]
        
        # Then try default (English) translations
        if key in self._default:
            print(f"Translation key '{key}' not found in requested locale for module '{self._module_name}', falling back to English")
            return self._default[key]
            
        # Finally try common translations
        if key in self._common:
            print(f"Translation key '{key}' not found in module '{self._module_name}' translations, falling back to common")
            return self._common[key]
            
        raise AttributeError(f"Translation key '{key}' not found in module '{self._module_name}'")

class I18n:
    def __init__(self, default_locale: str = 'en_US'):
        self.default_locale = default_locale
        self.translations: Dict[str, Dict[str, Dict[str, Any]]] = {}
        self.load_translations()

    def load_translations(self) -> None:
        """Load all translation files from the locales directory."""
        locales_dir = Path(__file__).parent / 'locales'
        if not locales_dir.exists():
            os.makedirs(locales_dir)
            
        # Load each JSON file in the locales directory
        for file in locales_dir.glob('*.json'):
            locale = file.stem  # filename without extension
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    self.translations[locale] = json.load(f)
            except json.JSONDecodeError:
                print(f"Error loading translation file: {file}")
                continue
            except FileNotFoundError:
                print(f"Translation file not found: {file}")
                continue

    def get(self, key: str, module: str = 'common', locale: str = 'en_US') -> Union[str, list, dict]:
        """
        Get a translation string.
        
        Args:
            key: The translation key
            module: The module/category the string belongs to (e.g., 'settings', 'help')
            locale: The locale to use
            
        Returns:
            The translated string/list/dict or the default language value if not found
        """
        try:
            # Try to get the string in the requested locale
            value = self.translations.get(locale, {}).get(module, {}).get(key)
            if value is not None:
                return value
                
            # Fallback to default locale
            return self.translations[self.default_locale][module][key]
        except KeyError:
            return f"Missing translation: {module}.{key}"

    def get_module(self, module: str, locale: str = 'en_US') -> TranslationModule:
        """
        Get all translations for a specific module.
        
        Args:
            module: The module/category to get translations for
            locale: The locale to use
            
        Returns:
            A TranslationModule object that allows accessing translations as attributes
        """
        try:
            # Get translations for the requested locale
            translations = self.translations.get(locale, {}).get(module, {})
            
            # Get default (English) translations for fallback
            default_translations = self.translations[self.default_locale].get(module, {})
            
            # Get common translations that apply to all modules
            common = {
                'error': 'An error occurred.',
                'version': 'version',
                'by': 'by',
                **self.translations.get(self.default_locale, {}).get('common', {}),  # English common first
                **self.translations.get(locale, {}).get('common', {})  # Then locale-specific common
            }
            
            return TranslationModule(translations, common, default_translations, module)
        except KeyError:
            return TranslationModule({}, {
                'error': 'An error occurred.',
                'version': 'version',
                'by': 'by'
            }, {}, module)

    def set_locale(self, user_id: int, locale: str) -> None:
        """Update user's preferred locale in the database."""
        from databases.database import set_lang  # Import here to avoid circular imports
        set_lang(user_id, locale)

    def get_locale(self, user_id: int) -> str:
        """Get user's preferred locale from the database."""
        from databases.database import get_lang  # Import here to avoid circular imports
        return get_lang(user_id)

# Global instance
i18n = I18n() 