import { SetMetadata, CustomDecorator } from '@nestjs/common';
import { UserMetadata } from '@src/enums/userMetadata';

export const Roles = (...roles: UserMetadata[]): CustomDecorator<string> => SetMetadata('roles', roles);