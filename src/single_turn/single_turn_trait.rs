use crate::errors::ModelError;
use async_trait::async_trait;

#[async_trait]
pub trait SingleTurnLlm {
    fn name(&self) -> &str;
    async fn generate(
        &self,
        prompt: String,
        preprompt: Option<String>,
    ) -> Result<String, ModelError>;
}